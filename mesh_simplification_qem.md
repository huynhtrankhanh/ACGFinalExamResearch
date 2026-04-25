# Mesh Simplification: Quadric Error Metrics (QEM)

**Reference:** Michael Garland and Paul Heckbert, "Surface Simplification Using Quadric Error Metrics," SIGGRAPH 97.

---

## 1. The Goal
To reduce the number of triangles in a mesh while minimizing the geometric deviation from the original surface. QEM is the industry standard for high-quality, fast simplification.

---

## 2. Core Operation: Edge Contraction
The algorithm simplifies the mesh by repeatedly applying **edge contraction** $(v_1, v_2) \to \bar{v}$.
- Two vertices $v_1, v_2$ are merged into a single new vertex $\bar{v}$.
- All triangles connected to $v_1$ or $v_2$ are updated to connect to $\bar{v}$.
- Degenerate triangles (that became edges or points) are removed.

---

## 3. The Quadric Error Metric

The "error" at a vertex $v$ is defined as the sum of squared distances to the set of planes associated with the vertex (the planes of the triangles that originally met there).

### 3.1 Plane Equation
A plane is defined by $ax + by + cz + d = 0$, where $a^2 + b^2 + c^2 = 1$.
We represent the plane as a vector $\mathbf{p} = [a, b, c, d]^T$.

### 3.2 Squared Distance to a Plane
The squared distance of a point $\mathbf{v} = [x, y, z, 1]^T$ to plane $\mathbf{p}$ is:
$$D^2(\mathbf{v}) = (\mathbf{p}^T \mathbf{v})^2 = \mathbf{v}^T (\mathbf{p} \mathbf{p}^T) \mathbf{v}$$

### 3.3 The Fundamental Error Quadric $\mathbf{K}_p$
For a single plane $\mathbf{p}$, the quadric matrix is the outer product:
$$\mathbf{K}_p = \mathbf{p} \mathbf{p}^T = \begin{bmatrix} a^2 & ab & ac & ad \\ ab & b^2 & bc & bd \\ ac & bc & c^2 & cd \\ ad & bd & cd & d^2 \end{bmatrix}$$

### 3.4 Vertex Quadric $\mathbf{Q}$
The error quadric for a vertex $v$ is the sum of the quadrics of all planes $p$ that meet at that vertex:
$$\mathbf{Q}_v = \sum_{p \in \text{planes}(v)} \mathbf{K}_p$$
Error at vertex $\mathbf{v}$ is simply: $\text{error}(\mathbf{v}) = \mathbf{v}^T \mathbf{Q}_v \mathbf{v}$.

---

## 4. The Algorithm Walkthrough

1. **Initialization:**
   - For every original vertex $v$, compute its initial quadric $\mathbf{Q}_v$ by summing the $\mathbf{K}_p$ of all adjacent triangle planes.
2. **Candidate Pairs:**
   - Select all edges $(v_1, v_2)$ as candidate pairs for contraction.
3. **Cost Calculation:**
   - For each pair $(v_1, v_2)$, compute the optimal position $\bar{v}$ that minimizes the error:
     $$\text{error}(\bar{v}) = \bar{v}^T (\mathbf{Q}_{v_1} + \mathbf{Q}_{v_2}) \bar{v}$$
   - **Finding Optimal $\bar{v}$:** Solve the linear system $\frac{\partial \text{error}}{\partial x} = \frac{\partial \text{error}}{\partial y} = \frac{\partial \text{error}}{\partial z} = 0$. This is equivalent to:
     $$\begin{bmatrix} q_{11} & q_{12} & q_{13} & q_{14} \\ q_{12} & q_{22} & q_{23} & q_{24} \\ q_{13} & q_{23} & q_{33} & q_{34} \\ 0 & 0 & 0 & 1 \end{bmatrix} \bar{v} = \begin{bmatrix} 0 \\ 0 \\ 0 \\ 1 \end{bmatrix}$$
     (If the matrix is non-invertible, use the midpoint or $v_1$ or $v_2$).
4. **Priority Queue:**
   - Place all pairs in a min-heap, keyed by their contraction cost (error).
5. **Iterative Simplification:**
   - While the target triangle count is not reached:
     - Pull the minimum cost pair $(v_1, v_2)$ from the heap.
     - Contract it to $\bar{v}$.
     - Update the quadric: $\mathbf{Q}_{\bar{v}} = \mathbf{Q}_{v_1} + \mathbf{Q}_{v_2}$.
     - Update the costs of all neighboring pairs that were connected to $v_1$ or $v_2$.

---

## 5. Key Advantages
- **Efficiency:** Summing quadrics is extremely fast.
- **Quality:** High-fidelity preservation of surface features and volume.
- **Visuals:** Naturally preserves "corners" and "edges" because the planes "intersecting" at those points create a high error penalty for moving away from them.
