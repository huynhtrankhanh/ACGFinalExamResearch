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
