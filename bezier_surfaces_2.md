This is a comprehensive guide on how to algorithmically compute Bézier curves, Bézier surfaces, and perform curve fitting. Bézier curves are foundational to computer graphics, animations, vector graphics, and Computer-Aided Design (CAD).
Here is the complete tutorial, broken down into mathematical theory, algorithmic implementation, and practical code examples.
## Part 1: The Bézier Curve
A Bézier curve is a parametric curve defined by a set of control points P_0, P_1, \dots, P_n. The curve always starts at P_0 and ends at P_n, while the intermediate points act as "magnets" that pull the curve toward them.
### 1. The Explicit Equation (Bernstein Polynomials)
The mathematical foundation of a Bézier curve of degree n is the sum of its control points weighted by **Bernstein polynomials**:
Where:
 * t is the parameter that goes from 0 to 1.
 * P_i are the control points.
 * \binom{n}{i} = \frac{n!}{i!(n-i)!} is the binomial coefficient.
While you *can* compute the curve using this explicit formula, calculating factorials for high-degree curves can lead to numerical instability and overflow. This is where De Casteljau's algorithm comes in.
### 2. De Casteljau's Algorithm
De Casteljau's algorithm evaluates a Bézier curve through **recursive linear interpolation**. It is numerically stable, robust, and geometrically intuitive.
**The Algorithm:**
 1. Treat your initial control points as the "zero-th" level: P_i^{(0)} = P_i.
 2. For a given t (where 0 \le t \le 1), compute the next level of points by linearly interpolating between adjacent points:
   
 3. Repeat this process until you are left with a single point: P_0^{(n)}. This point is exactly B(t).
**Python Implementation:**
```python
def de_casteljau(control_points, t):
    """
    Evaluates a Bezier curve at parameter t using De Casteljau's algorithm.
    control_points: List of (x, y) tuples.
    t: Float between 0.0 and 1.0.
    """
    # Create a working copy of the control points
    points = list(control_points)
    n = len(points) - 1
    
    for j in range(1, n + 1):
        for i in range(n - j + 1):
            x = (1 - t) * points[i][0] + t * points[i+1][0]
            y = (1 - t) * points[i][1] + t * points[i+1][1]
            points[i] = (x, y)
            
    # The final remaining point is the point on the curve at t
    return points[0]

# Example: Compute a cubic curve at t=0.5
pts = [(0, 0), (0, 1), (1, 1), (1, 0)]
point_at_half = de_casteljau(pts, 0.5)

```
## Part 2: The Bézier Surface
A Bézier surface is the 3D extension of a Bézier curve. Instead of a 1D line of control points, you use a 2D grid of control points P_{i,j} of size (n+1) \times (m+1). The surface is evaluated using two parameters, u and v, both ranging from 0 to 1.
### 1. The Surface Equation
A Bézier surface is the tensor product of two Bézier curves:
Where B_i^n(u) and B_j^m(v) are the Bernstein basis polynomials.
### 2. Algorithmic Computation (Nested De Casteljau)
To find a point on the surface S(u, v), you don't need a complex new algorithm. You simply apply De Casteljau's algorithm in two passes:
 1. **Row-wise reduction:** For every row i in your control grid, treat the points in that row as a Bézier curve. Run De Casteljau on each row with the parameter u. This leaves you with a single column of n+1 intermediate points.
 2. **Column-wise reduction:** Take that newly generated column of points. Treat them as a single Bézier curve and run De Casteljau with the parameter v. The final resulting point is your surface point S(u, v).
**Python Implementation:**
```python
def bezier_surface(control_grid, u, v):
    """
    Evaluates a Bezier surface at (u, v).
    control_grid: 2D list (list of lists) of (x, y, z) control points.
    """
    u_curve_points = []
    
    # Pass 1: Evaluate De Casteljau along the 'u' direction for each row
    for row in control_grid:
        point_u = de_casteljau_3d(row, u) # Assume de_casteljau_3d handles 3D tuples
        u_curve_points.append(point_u)
        
    # Pass 2: Evaluate De Casteljau along the 'v' direction using the results
    final_surface_point = de_casteljau_3d(u_curve_points, v)
    
    return final_surface_point

```
## Part 3: Curve Fitting with Bézier Curves
Curve fitting is the inverse problem: You have a large set of data points D_0, D_1, \dots, D_m (like a user's mouse drawing or a noisy data scan), and you want to find a smaller set of Bézier control points P_0, \dots, P_n that accurately approximate the data.
Because we usually want fewer control points than data points (n < m), an exact match isn't possible. Instead, we use **Least Squares Optimization**.
### Step 1: Parameterize the Data Points
To compare our data points to a Bézier curve, we must assign a t_k value (between 0 and 1) to each data point D_k.
The easiest stable method is **Chord-Length Parameterization**. We calculate the cumulative distance between points:
 1.  2. Calculate total length L = \sum_{k=1}^{m} |D_k - D_{k-1}|
 3. Assign t_k = t_{k-1} + \frac{|D_k - D_{k-1}|}{L}
 4. ### Step 2: Set Up the Linear System
We want our Bézier curve B(t_k) to match our data points D_k:
We can represent this as a matrix equation:

Where:
 * \mathbf{D} is an m \times 2 (or 3) matrix of the target data points.
 * \mathbf{P} is an n \times 2 matrix of the unknown control points we want to find.
 * \mathbf{M} is an m \times n matrix where each element M_{k,i} is the Bernstein polynomial B_i^n(t_k).
### Step 3: Solve Using Least Squares
Since \mathbf{M} is not a square matrix, we cannot simply invert it. Instead, we multiply both sides by the transpose \mathbf{M}^T to create the **Normal Equations**:
Now, (\mathbf{M}^T \mathbf{M}) is a square, invertible matrix. We solve for the control points \mathbf{P}:
**Python Implementation (using NumPy):**
```python
import numpy as np
import math

def bernstein_poly(n, i, t):
    """Computes the Bernstein polynomial B_{i,n}(t)."""
    return math.comb(n, i) * (t**i) * ((1 - t)**(n - i))

def fit_bezier_curve(data_points, degree):
    """
    Fits a Bezier curve of a given degree to a set of data points.
    data_points: numpy array of shape (m, 2)
    degree: integer n
    """
    m = len(data_points)
    n = degree
    
    # 1. Chord-length parameterization
    t_values = np.zeros(m)
    distances = np.linalg.norm(np.diff(data_points, axis=0), axis=1)
    cumulative_dist = np.insert(np.cumsum(distances), 0, 0)
    t_values = cumulative_dist / cumulative_dist[-1]
    
    # 2. Build the Matrix M
    M = np.zeros((m, n + 1))
    for k in range(m):
        for i in range(n + 1):
            M[k, i] = bernstein_poly(n, i, t_values[k])
            
    # 3. Solve the Normal Equations: P = (M^T * M)^-1 * M^T * D
    # Note: np.linalg.lstsq does this efficiently and handles edge cases
    P, residuals, rank, s = np.linalg.lstsq(M, data_points, rcond=None)
    
    # Ensure exact endpoint matching (optional but highly recommended)
    P[0] = data_points[0]
    P[-1] = data_points[-1]
    
    return P

```
Here are the full TypeScript implementations for De Casteljau's algorithm in both 2D and 3D.
To take advantage of TypeScript, we will first define clear interfaces for our data structures. The algorithm itself relies on an iterative approach, creating a working copy of the array and reducing it level by level until only the final evaluated point remains.
### 1. Defining the Types
First, we define the strict types for our 2D and 3D points so the compiler can catch any missing coordinates.
```typescript
export interface Point2D {
    x: number;
    y: number;
}

export interface Point3D extends Point2D {
    z: number;
}

```
### 2. De Casteljau for 2D Points
This function takes an array of Point2D objects and a parameter t (where 0 \le t \le 1). It interpolates the x and y coordinates.
```typescript
/**
 * Evaluates a point on a 2D Bezier curve using De Casteljau's algorithm.
 * * @param points - An array of 2D control points.
 * @param t - The parameter t, typically between 0.0 and 1.0.
 * @returns The evaluated 2D point on the curve.
 */
export function deCasteljau2D(points: Point2D[], t: number): Point2D {
    if (points.length === 0) {
        throw new Error("At least one control point is required.");
    }
    
    // Create a deep copy of the points to avoid mutating the original array
    const workingPoints: Point2D[] = points.map(p => ({ x: p.x, y: p.y }));
    const n = workingPoints.length - 1;

    // Iteratively reduce the points
    for (let j = 1; j <= n; j++) {
        for (let i = 0; i <= n - j; i++) {
            workingPoints[i] = {
                x: (1 - t) * workingPoints[i].x + t * workingPoints[i + 1].x,
                y: (1 - t) * workingPoints[i].y + t * workingPoints[i + 1].y
            };
        }
    }

    // The final remaining point is the evaluated point
    return workingPoints[0];
}

```
### 3. De Casteljau for 3D Points
The 3D version is identical in structure to the 2D version, but it includes the z-axis in the linear interpolation step.
```typescript
/**
 * Evaluates a point on a 3D Bezier curve using De Casteljau's algorithm.
 * * @param points - An array of 3D control points.
 * @param t - The parameter t, typically between 0.0 and 1.0.
 * @returns The evaluated 3D point on the curve.
 */
export function deCasteljau3D(points: Point3D[], t: number): Point3D {
    if (points.length === 0) {
        throw new Error("At least one control point is required.");
    }
    
    // Create a deep copy of the points
    const workingPoints: Point3D[] = points.map(p => ({ x: p.x, y: p.y, z: p.z }));
    const n = workingPoints.length - 1;

    // Iteratively reduce the points
    for (let j = 1; j <= n; j++) {
        for (let i = 0; i <= n - j; i++) {
            workingPoints[i] = {
                x: (1 - t) * workingPoints[i].x + t * workingPoints[i + 1].x,
                y: (1 - t) * workingPoints[i].y + t * workingPoints[i + 1].y,
                z: (1 - t) * workingPoints[i].z + t * workingPoints[i + 1].z
            };
        }
    }

    return workingPoints[0];
}

```
### Usage Example
Here is how you would call these functions in your TypeScript application:
```typescript
// 2D Example: A simple quadratic curve
const curve2D: Point2D[] = [
    { x: 0, y: 0 },
    { x: 5, y: 10 },
    { x: 10, y: 0 }
];

// Evaluate exactly at the halfway mark
const midpoint2D = deCasteljau2D(curve2D, 0.5);
console.log(`2D Point at t=0.5: (${midpoint2D.x}, ${midpoint2D.y})`); 
// Output: 2D Point at t=0.5: (5, 5)


// 3D Example: A cubic curve in 3D space
const curve3D: Point3D[] = [
    { x: 0, y: 0, z: 0 },
    { x: 0, y: 10, z: 5 },
    { x: 10, y: 10, z: 10 },
    { x: 10, y: 0, z: 15 }
];

// Evaluate at 75% along the curve
const point3D = deCasteljau3D(curve3D, 0.75);
console.log(`3D Point at t=0.75: (${point3D.x}, ${point3D.y}, ${point3D.z})`);

```
To compute a point on a Bézier surface, we apply De Casteljau's algorithm in two dimensions. You can think of a Bézier surface as a grid of control points. First, we use the parameter u to evaluate a point along each row of the grid. This yields a new, single "column" of intermediate points. Then, we use the parameter v to evaluate that new column, which gives us our final 3D point on the surface.
Here is the complete, self-contained TypeScript code to evaluate a Bézier surface, including a function to generate a full mesh of points so you can render it.
### 1. The Bézier Surface Implementation
```typescript
export interface Point3D {
    x: number;
    y: number;
    z: number;
}

/**
 * Helper function: De Casteljau's algorithm for a 1D curve in 3D space.
 */
function deCasteljau3D(points: Point3D[], t: number): Point3D {
    if (points.length === 0) {
        throw new Error("At least one control point is required.");
    }
    
    const workingPoints: Point3D[] = points.map(p => ({ x: p.x, y: p.y, z: p.z }));
    const n = workingPoints.length - 1;

    for (let j = 1; j <= n; j++) {
        for (let i = 0; i <= n - j; i++) {
            workingPoints[i] = {
                x: (1 - t) * workingPoints[i].x + t * workingPoints[i + 1].x,
                y: (1 - t) * workingPoints[i].y + t * workingPoints[i + 1].y,
                z: (1 - t) * workingPoints[i].z + t * workingPoints[i + 1].z
            };
        }
    }

    return workingPoints[0];
}

/**
 * Evaluates a specific (u, v) point on a Bezier surface.
 * @param controlGrid - A 2D array [row][col] of 3D control points.
 * @param u - The parameter u, typically between 0.0 and 1.0.
 * @param v - The parameter v, typically between 0.0 and 1.0.
 * @returns The evaluated 3D point on the surface.
 */
export function evaluateBezierSurface(controlGrid: Point3D[][], u: number, v: number): Point3D {
    if (controlGrid.length === 0 || controlGrid[0].length === 0) {
        throw new Error("Control grid cannot be empty.");
    }

    const uCurvePoints: Point3D[] = [];

    // Step 1: Reduce each row of the grid into a single point using parameter 'u'
    for (let i = 0; i < controlGrid.length; i++) {
        const pointAtU = deCasteljau3D(controlGrid[i], u);
        uCurvePoints.push(pointAtU);
    }

    // Step 2: Reduce the resulting column of points into a final point using parameter 'v'
    return deCasteljau3D(uCurvePoints, v);
}

/**
 * Generates a full mesh/grid of points representing the Bezier surface.
 * Useful for rendering the surface in a 3D engine like Three.js.
 * @param controlGrid - A 2D array [row][col] of 3D control points.
 * @param resolution - How many segments to divide the surface into.
 * @returns A 2D array of points representing the final evaluated surface.
 */
export function generateSurfaceMesh(controlGrid: Point3D[][], resolution: number): Point3D[][] {
    const surfaceMesh: Point3D[][] = [];

    for (let i = 0; i <= resolution; i++) {
        const u = i / resolution;
        const row: Point3D[] = [];
        
        for (let j = 0; j <= resolution; j++) {
            const v = j / resolution;
            row.push(evaluateBezierSurface(controlGrid, u, v));
        }
        
        surfaceMesh.push(row);
    }

    return surfaceMesh;
}

```
### 2. Usage Example
To test this, we can define a biquadratic surface (a 3 \times 3 grid of control points). This creates a simple curved "sheet" in 3D space.
```typescript
// Define a 3x3 grid of control points (Biquadratic Bezier Surface)
const surfaceControlGrid: Point3D[][] = [
    // Row 0
    [ {x: -10, y: -10, z: 0}, {x: 0, y: -10, z: 5}, {x: 10, y: -10, z: 0} ],
    // Row 1
    [ {x: -10, y: 0, z: 5},   {x: 0, y: 0, z: 10},  {x: 10, y: 0, z: 5}   ],
    // Row 2
    [ {x: -10, y: 10, z: 0},  {x: 0, y: 10, z: 5},  {x: 10, y: 10, z: 0}  ]
];

// 1. Evaluate a single point in the dead center of the surface
const centerPoint = evaluateBezierSurface(surfaceControlGrid, 0.5, 0.5);
console.log(`Center point (u=0.5, v=0.5): x=${centerPoint.x}, y=${centerPoint.y}, z=${centerPoint.z}`);
// Output: Center point (u=0.5, v=0.5): x=0, y=0, z=6.25

// 2. Generate a coarse mesh (4x4 points) for rendering
const resolution = 3; // 3 segments means 4 points along each axis
const mesh = generateSurfaceMesh(surfaceControlGrid, resolution);

console.log(`\nGenerated Mesh (${mesh.length}x${mesh[0].length}):`);
console.log(`Point at u=1, v=1: x=${mesh[3][3].x}, y=${mesh[3][3].y}, z=${mesh[3][3].z}`);
// Output will match the bottom-right corner control point: x=10, y=10, z=0

```
