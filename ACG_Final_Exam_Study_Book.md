# Advanced Computer Graphics — Final Exam Comprehensive Study Book

**Course:** Advanced Computer Graphics (ACG)  
**Prepared from:** Final Exam Transcript + Deep Literature Research + Assignment 3 Papers
**Format:** Open Book, Open Notes · Paper Only · No Electronics  
**Exam Structure:** 5 Questions (3 Theory + 2 Computation) · 2 Hours

---

> *This book is designed to be printed and brought into the examination. Every topic mentioned in the professor's final review lecture is covered in depth, with algorithms, examples, and detailed mathematical computation walkthroughs.*

---

## Table of Contents

1. [Virtual Reality (VR) and Augmented Reality (AR)](#chapter-1)
   - 1.1 Definitions and Continuum
   - 1.2 VR Subsystems and Performance
   - 1.3 AR Tracking (PnP and SLAM Pipelines)
2. [Geometric Modeling](#chapter-2)
   - 2.1 Point Clouds and Spatial Structures
   - 2.2 Triangulation (Delaunay, BPA, Poisson)
   - 2.3 Mesh Simplification (Quadric Error Metrics Math)
   - 2.4 Hole Filling (Ear Clipping, Min-Area DP)
   - 2.5 Noise Removal (SOR, Moving Least Squares Math)
3. [Medical Image Processing](#chapter-3)
   - 3.1 CT Scanning (Physics and FBP Reconstruction)
   - 3.2 MRI Scanning (Physics and FFT Reconstruction)
   - 3.3 3D Reconstruction Pipeline
   - 3.4 Brain Tumor Detection (BraTS and U-Net)
   - 3.5 Assignment 3: Intensity-Curvature Measurement Approaches
4. [Curves and Surfaces — The Key Math](#chapter-4)
   - 4.1 Bézier Curves
   - 4.2 Bézier Surfaces
   - 4.3 De Casteljau's Algorithm
   - 4.4 Worked Computation Examples (including Degree-5 Example)

---

# Chapter 1 — Virtual Reality (VR) and Augmented Reality (AR) {#chapter-1}

## 1.1 Definitions and the Reality–Virtuality Continuum
- **Virtual Reality (VR):** Fully synthetic environment.
- **Augmented Reality (AR):** Virtual overlay on the real world.
- **Mixed Reality (MR):** Virtual and real objects interact.
- **Reality–Virtuality Continuum (Milgram 1994):**
  `Real Environment <--> AR <--> MR <--> Augmented Virtuality <--> VR`

## 1.2 VR Subsystems and Performance
- **Tracking:** 6 Degrees of Freedom (6-DoF) required: X, Y, Z (translation) + Pitch, Yaw, Roll (rotation).
- **Latency:** Motion-to-photon latency must be **< 20 ms** to prevent motion sickness.
- **Rendering:**
  - **Foveated rendering:** Render at high resolution only where the eye is looking (the fovea), saving 30-70% GPU cost.
  - **Asynchronous Timewarp (ATW):** Warps the last frame if a new one isn't ready, preventing judder.
- **Displays:**
  - **Vergence-Accommodation Conflict (VAC):** Eyes converge at depth but focus at the screen's fixed distance, causing strain.

## 1.3 AR Tracking Methods

### 1.3.1 Marker-Based AR (The PnP Problem)
**PnP (Perspective-n-Point)** estimates the pose of a camera given $n$ 3D points and their 2D projections.
- **Input:** Known 3D corners $P_i$ and observed 2D points $u_i$.
- **Goal:** Find Rotation $R$ and Translation $t$.
- **Optimization:** $\min_{R,t} \sum \| u_i - \text{project}(K, R, t, P_i) \|^2$.

### 1.3.2 Markerless AR (SLAM Pipeline)
**SLAM (Simultaneous Localization and Mapping)** builds a map while tracking pose.
1. **Feature Extraction:** Find keypoints (ORB, SIFT).
2. **Data Association:** Match features to the existing 3D map.
3. **Pose Tracking:** Solve PnP using matched points.
4. **Mapping:** Triangulate new 3D points.
5. **Bundle Adjustment:** Globally optimize poses and points: $\min \sum \| \text{reprojection\_error} \|^2$.
6. **Loop Closure:** Detect and correct drift when returning to a known location.

---

# Chapter 2 — Geometric Modeling {#chapter-2}

## 2.1 Point Clouds
- **Acquisition:** LiDAR, Structured Light, Photogrammetry.
- **Normal Estimation:** PCA on $k$-nearest neighbors. The normal is the eigenvector of the smallest eigenvalue of the covariance matrix.

## 2.2 Triangulation
- **Delaunay (2D):** No point lies inside any triangle's circumcircle. Maximizes the minimum angle.
- **Ball Pivoting (3D):** Rolls a sphere of radius $\rho$ over points to form triangles.
- **Poisson Surface Reconstruction:** Global method solving $\nabla^2 \chi = \nabla \cdot \vec{V}$ where $\chi$ is an indicator function and $\vec{V}$ is the normal field. Extracts a "watertight" mesh.

## 2.3 Mesh Simplification: Quadric Error Metrics (QEM)
The core operation is **edge contraction** $(v_1, v_2) \to \bar{v}$.
- **Math:** For a plane $\mathbf{p} = [a, b, c, d]^T$, the error quadric is $\mathbf{K}_p = \mathbf{p} \mathbf{p}^T$.
- **Vertex Quadric:** $\mathbf{Q}_v = \sum \mathbf{K}_p$ for all adjacent planes.
- **Cost:** $\text{error}(\bar{v}) = \bar{v}^T (\mathbf{Q}_{v1} + \mathbf{Q}_{v2}) \bar{v}$.
- **Optimal $\bar{v}$:** Found by solving $\nabla(\text{error}) = 0$.

## 2.4 Hole Filling
- **Ear Clipping:** Local, simple triangulation of boundary loops.
- **Minimum-Area Triangulation:** Uses Dynamic Programming to find the triangulation minimizing total area.
  $E(i, j) = \min_{k} [ E(i, k) + E(k, j) + \text{Area}(v_i, v_k, v_j) ]$.
- **Refinement:** Laplacian smoothing $v_i \leftarrow \frac{1}{|N|} \sum v_j$ to match surrounding curvature.

## 2.5 Noise Removal & Regularization
- **SOR (Statistical Outlier Removal):** Removes points with mean neighbor distance $> \mu + \alpha \sigma$.
- **Moving Least Squares (MLS):** Fits local polynomials to neighborhoods and projects points onto them. Smooths noise while preserving surface structure.
- **Voxel Downsampling:** Replaces all points in a voxel with their centroid for uniform density.

---

# Chapter 3 — Medical Image Processing {#chapter-3}

## 3.1 CT Scanning
- **Physics:** X-ray attenuation measured in **Hounsfield Units (HU)**. Air = -1000, Water = 0, Bone = +1000.
- **Reconstruction:** **Filtered Back-Projection (FBP)** using the Radon transform and a ramp filter $|f|$ to avoid blurring.

## 3.2 MRI Scanning
- **Physics:** Nuclear Magnetic Resonance (NMR) of protons.
- **Reconstruction:** 2D Inverse Fourier Transform of collected **k-space** data.
- **Sequences:** T1 (anatomy), T2 (pathology/edema), FLAIR (CSF suppressed), DWI (stroke/cellularity).

## 3.3 3D Reconstruction Pipeline
`Scan -> DICOM -> Segmentation (U-Net) -> Marching Cubes -> Post-processing (QEM/Smoothing) -> 3D Mesh`.

## 3.4 Brain Tumor Detection
- **Sub-regions:** Whole Tumor (WT), Tumor Core (TC), Enhancing Tumor (ET).
- **Metric:** **Dice Score** $= \frac{2 |A \cap B|}{|A| + |B|}$.

## 3.5 Assignment 3: Intensity-Curvature (IC) Approaches
Research by **Carlo Ciulla** focuses on extracting hidden details via higher-order derivatives.
- **Classic-Curvature (CC) & ICF:** Create a **"Visually Perceptible Third Dimension"** perpendicular to the image plane, showing signal "geography" (elevations/valleys).
- **Signal Resilient to Interpolation (SRI):** Acts as an **"Internal Light Bulb"**, stretching grayscale to illuminate fine tumor textures and distinguish solid vs. cystic parts.
- **Impact:** Does not require segmentation; provides a "medical intensity-curvature measure map" for radiologists.

---

# Chapter 4 — Curves and Surfaces: The Key Math {#chapter-4}

## 4.1 Bézier Curves
- **Formula:** $B(t) = \sum_{i=0}^n \binom{n}{i} (1-t)^{n-i} t^i P_i$.
- **Cubic (n=3):** $B(t) = (1-t)^3 P_0 + 3(1-t)^2 t P_1 + 3(1-t) t^2 P_2 + t^3 P_3$.
- **Tangents:** $B'(0) = n(P_1 - P_0)$; $B'(1) = n(P_n - P_{n-1})$.

## 4.2 Bézier Surfaces
- **Tensor Product:** $B(u,v) = \sum \sum B_{i,m}(u) B_{j,n}(v) P_{i,j}$.
- **Evaluation:** Apply De Casteljau in $u$, then in $v$ on the resulting points.

## 4.3 De Casteljau's Algorithm
- **Recurrence:** $P_i^{(j)} = (1-t) P_i^{(j-1)} + t P_{i+1}^{(j-1)}$.
- **Triangle Scheme:**
  ```
  P0 --(lerp)--> Q0 --(lerp)--> R0 (Answer)
  P1 --(lerp)--> Q1
  P2
  ```

## 4.4 Worked Computation Example: Degree-5 (Quintic)
**Given:** $P_0(0,0), P_1(1,0), P_2(2,1), P_3(3,1), P_4(4,0), P_5(5,0)$ at **t = 0.75**.
1. **Level 1 (j=1):** $Q_0=(0.75,0), Q_1=(1.75,0.75), Q_2=(2.75,1), Q_3=(3.75,0.25), Q_4=(4.75,0)$.
2. **Level 2 (j=2):** $R_0=(1.5, 0.5625), R_1=(2.5, 0.9375), R_2=(3.5, 0.4375), R_3=(4.5, 0.0625)$.
3. **Level 3 (j=3):** $S_0=(2.25, 0.84375), S_1=(3.25, 0.5625), S_2=(4.25, 0.15625)$.
4. **Level 4 (j=4):** $T_0=(3, 0.6328), T_1=(4, 0.2578)$.
5. **Level 5 (j=5):** $U_0 = (3.75, 0.3516)$ -> **Final Answer**.

---
*End of Study Book · Success on the Exam!*
