# Surface Reconstruction: Poisson Surface Reconstruction

**Reference:** Michael Kazhdan, Matthew Bolitho, and Hugues Hoppe, "Poisson Surface Reconstruction," SGP 2006.

---

## 1. The Core Idea
Poisson reconstruction is a **global** method for turning an oriented point cloud into a "watertight" triangle mesh. Unlike local methods (like Ball Pivoting), it considers all points simultaneously by solving a partial differential equation.

It treats the problem as a **spatial Poisson problem**:
- Find an indicator function $\chi$ (where $\chi=1$ inside the model and $\chi=0$ outside).
- The gradient of this indicator function $\nabla \chi$ should match the oriented normals $\vec{V}$ of the input points.

---

## 2. Mathematical Formulation

### 2.1 The Indicator Function
The goal is to find a scalar function $\chi(x,y,z)$ such that:
$$\chi(p) = \begin{cases} 1 & \text{if } p \in \text{Solid} \\ 0 & \text{if } p \notin \text{Solid} \end{cases}$$

### 2.2 Relationship to Normals
The gradient of the indicator function $\nabla \chi$ is a vector field that is zero everywhere except at the surface, where it points inward and has a magnitude equal to a Dirac delta function.
Therefore, if we have oriented normals $\vec{V}$ from our point cloud, we want:
$$\nabla \chi \approx \vec{V}$$

### 2.3 The Poisson Equation
Applying the divergence operator ($\nabla \cdot$) to both sides, we get the Poisson equation:
$$\nabla \cdot (\nabla \chi) = \nabla \cdot \vec{V}$$
$$\boxed{\nabla^2 \chi = \nabla \cdot \vec{V}}$$
Where $\nabla^2$ is the **Laplacian operator**.

---

## 3. The Algorithm Steps

1. **Normal Estimation:**
   - If the point cloud doesn't have normals, estimate them using PCA on local neighborhoods (e.g., $k$-nearest neighbors).
   - Ensure normals are consistently oriented (all pointing out).

2. **Vector Field Construction:**
   - Define a continuous vector field $\vec{V}$ by smoothing the input point normals using a kernel (typically a Gaussian or B-spline).

3. **Solve the Poisson Equation:**
   - Discretize the space using an **Octree** (finer resolution near points, coarser far away).
   - Solve the linear system $\mathbf{L}x = b$ where $\mathbf{L}$ is the Laplacian matrix and $b$ is the divergence of the normal field.

4. **Isosurface Extraction:**
   - Once $\chi$ is computed for all voxels/nodes, extract the surface where $\chi = 0.5$ using the **Marching Cubes** algorithm.

---

## 4. Why Use Poisson Reconstruction?

| Feature | Advantage |
|---|---|
| **Global Optimization** | Robust to noise and outliers (averages out local errors). |
| **Watertight** | Guaranteed to produce a closed, manifold mesh with no holes. |
| **Resilient to Holes** | Naturally "bridges" gaps in the point cloud where data is missing. |
| **Smoothness** | Produces high-quality, smooth surfaces. |

**Comparison to Ball Pivoting:**
- **Ball Pivoting:** Fast, preserves exact point locations, but fails if points are sparse or noisy (creates holes).
- **Poisson:** Slower, may "shrink" or "expand" slightly (approximating), but creates a perfect solid mesh even from poor data.
