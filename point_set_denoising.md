# Point Set Denoising and Regularization

Point clouds acquired from scanners often contain **noise** (random displacement) and **outliers** (completely incorrect points). Geometric modeling requires these to be removed to ensure a clean mesh reconstruction.

---

## 1. Outlier Removal

Outliers are points that do not belong to the surface (e.g., reflections, dust).

### 1.1 Statistical Outlier Removal (SOR)
For each point $p_i$:
1. Find $k$ nearest neighbors.
2. Calculate the mean distance $\mu_i$ to neighbors.
3. Compute the global mean $\mu$ and standard deviation $\sigma$ of these distances.
4. **Remove $p_i$** if $\mu_i > \mu + \alpha \cdot \sigma$ (where $\alpha$ is a threshold, e.g., 2.0).

### 1.2 Radius Outlier Removal
Remove points that have fewer than $n$ neighbors within a fixed radius $r$.

---

## 2. Point Denoising (Smoothing)

Denoising reduces high-frequency jitter while preserving the underlying surface.

### 2.1 Moving Least Squares (MLS)
The gold standard for point cloud smoothing.
- For each point $p_i$, fit a local **polynomial surface** (often a plane) to its $k$-nearest neighbors using weighted least squares.
- Weights are usually Gaussian: $w_j = \exp(-d_j^2 / h^2)$, where $d_j$ is the distance to the neighbor.
- **Project $p_i$** onto the fitted surface.
- Result: Points are moved onto a smooth, implicit surface.

### 2.2 Bilateral Filtering for Points
Borrowed from image processing. It smooths points based on both spatial distance and **normal similarity**.
- Prevents "blurring" of sharp edges.
- Points are moved only along their normal direction.

---

## 3. Point Set Regularization (Resampling)

Ensures the point cloud has a uniform density, which is critical for algorithms like Poisson reconstruction.

### 3.1 Voxel Downsampling
1. Create a 3D voxel grid over the point cloud.
2. In each voxel cell, replace all points with their **centroid**.
3. Result: One point per non-empty voxel, uniform spacing.

### 3.2 Upsampling (MLS-based)
To increase density, the MLS surface is evaluated at additional locations (e.g., by jittering existing points and projecting them back to the MLS surface).

---

## 4. Summary Table

| Goal | Algorithm | Key Idea |
|---|---|---|
| **Remove Outliers** | SOR | Statistics of neighbor distances |
| **Remove Outliers** | Radius Search | Density thresholding |
| **Smooth Noise** | MLS | Fit local polynomial + project |
| **Preserve Edges** | Bilateral Filter | Weight by normal similarity |
| **Uniform Density** | Voxel Grid | Replace cell points with centroid |
| **Increase Density**| MLS Upsampling | Evaluate surface at new points |
