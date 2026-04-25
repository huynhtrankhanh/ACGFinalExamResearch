# Advanced Computer Graphics — Final Exam Comprehensive Study Book

**Course:** Advanced Computer Graphics (ACG)  
**Prepared from:** Final Exam Transcript + Deep Literature Research  
**Format:** Open Book, Open Notes · Paper Only · No Electronics  
**Exam Structure:** 5 Questions (3 Theory + 2 Computation) · 2 Hours

---

> *This book is designed to be printed and brought into the examination. Every topic mentioned in the professor's final review lecture is covered in depth, with algorithms, examples, and computation walkthroughs.*

---

## Table of Contents

1. [Virtual Reality (VR) and Augmented Reality (AR)](#chapter-1)
2. [Geometric Modeling](#chapter-2)
   - 2.1 Point Clouds
   - 2.2 Triangulation
   - 2.3 Mesh Simplification
   - 2.4 Hole Filling & Surface Reconstruction
   - 2.5 Noise Removal & Point Set Regularization
3. [Medical Image Processing](#chapter-3)
   - 3.1 CT Scanning
   - 3.2 MRI Scanning
   - 3.3 3D Reconstruction from Medical Scans
   - 3.4 Brain Tumor Detection
4. [Curves and Surfaces — The Key Math](#chapter-4)
   - 4.1 Bézier Curves
   - 4.2 Bézier Surfaces
   - 4.3 De Casteljau's Algorithm
   - 4.4 Worked Computation Examples

---

# Chapter 1 — Virtual Reality (VR) and Augmented Reality (AR) {#chapter-1}

## 1.1 Definitions and the Reality–Virtuality Continuum

**Virtual Reality (VR)** is a fully simulated, computer-generated environment that replaces the user's real-world perception. The user is immersed in a 3D digital world through a head-mounted display (HMD) with tracking sensors, auditory feedback, and sometimes haptic feedback.

**Augmented Reality (AR)** overlays computer-generated content (images, 3D objects, annotations) onto the real world in real time. The user continues to see the real world, but with digital enhancements layered on top.

**Mixed Reality (MR)** is sometimes used as a synonym for AR or as a distinct category where virtual and real objects coexist and interact.

Paul Milgram's **Reality–Virtuality Continuum (1994)** arranges these on a spectrum:

```
Real Environment ←——————————————————→ Virtual Environment
                  AR     MR     AV
```

- **AR (Augmented Reality):** Mostly real, supplemented by virtual
- **AV (Augmented Virtuality):** Mostly virtual, supplemented by real elements
- **VR:** Completely virtual

## 1.2 How VR Systems Work

A VR system has four critical subsystems:

### 1.2.1 Tracking and Pose Estimation
The system must know exactly where the user's head (and hands) are at all times.

- **6 Degrees of Freedom (6-DoF):** Three translational (x, y, z) + three rotational (pitch, yaw, roll)
- **Inside-out tracking:** Cameras on the headset observe the environment (Meta Quest, HoloLens)
- **Outside-in tracking:** External base stations emit infrared light or radio signals that the headset detects (Valve Index, original HTC Vive)
- **IMU (Inertial Measurement Unit):** Accelerometer + gyroscope for fast rotational tracking; fused with visual tracking via a Kalman filter

### 1.2.2 Rendering Pipeline
VR requires **two images** (one per eye) rendered at very high frame rates:

| Requirement | Typical Specification |
|---|---|
| Minimum frame rate | 72 fps (discomfort below this) |
| Ideal frame rate | 90–120 fps |
| Resolution per eye | 2000×2000 pixels (modern headsets) |
| Latency (motion-to-photon) | <20 ms (to prevent nausea) |

**Foveated rendering:** Because the eye's fovea (high-acuity region) covers only ~2° of visual field, eye-tracking allows the GPU to render only the gaze point in full resolution, reducing GPU load by 30–70%.

**Reprojection / Asynchronous Timewarp (ATW):** If a frame is late, the GPU extrapolates the new head orientation from the pose data and warps the previous frame rather than displaying a stale or missing image. This prevents judder.

### 1.2.3 Display Technologies
- **LCD:** Fast-switching IPS panels used in many consumer headsets
- **OLED:** Higher contrast, true blacks, but risk of persistence/ghosting; used in PlayStation VR
- **Pancake Optics:** Fold light back and forth to create thin lenses (Meta Quest 3, Apple Vision Pro)
- **Fresnel Lenses:** Lightweight concentric rings that approximate a convex lens

**Vergence-Accommodation Conflict (VAC):** In natural vision, the eyes both converge (rotate inward) and accommodate (focus) to the same distance. Current VR displays fix the focal plane at a single depth (~2 m), so the eyes converge at a virtual object's depth but accommodate to the fixed screen distance. This causes fatigue. Light field displays and varifocal displays aim to solve this.

### 1.2.4 VR Software Pipeline

```
User Input (HMD + Controllers)
         ↓
Pose Tracking + Prediction
         ↓
Scene Graph Update (Physics, AI, Scripting)
         ↓
Frustum Culling & Level of Detail (LOD) Selection
         ↓
GPU Rendering (Vertex Shader → Rasterization → Fragment Shader)
         ↓
Post-Processing (Lens Distortion Correction, Chromatic Aberration)
         ↓
Display (Left Eye | Right Eye)
```

**Key VR engines:** Unity 3D, Unreal Engine, Godot  
**Key VR APIs:** OpenXR (cross-platform), OpenVR (SteamVR), Meta XR SDK

## 1.3 How AR Systems Work

AR must solve two core problems: **tracking** (where am I in the world?) and **rendering** (how do I blend virtual and real visually?).

### 1.3.1 AR Tracking Methods

**Marker-Based AR:**  
- Fiducial markers (ArUco, QR codes, Vuforia targets) are recognized by computer vision
- The known marker geometry allows computing camera pose via PnP (Perspective-n-Point) algorithm
- Simple, fast, but requires a physical marker

**Markerless AR (SLAM-based):**  
- SLAM = Simultaneous Localization and Mapping
- The device builds a map of the environment while simultaneously localizing itself within it
- Feature points (SIFT, ORB, FAST) are extracted from camera frames; matched frame-to-frame
- **ARKit** (Apple) and **ARCore** (Google) implement SLAM + Visual-Inertial Odometry (VIO) on phones

**Plane Detection:**  
ARKit/ARCore detect horizontal and vertical planes using depth sensors or monocular depth estimation, enabling virtual objects to sit on surfaces.

**LiDAR-based depth scanning (iPhone 12 Pro+, iPad Pro):**  
Direct depth measurement allows instant surface reconstruction, occlusion handling, and faster SLAM initialization.

### 1.3.2 Registration and Rendering in AR

**Registration** = aligning virtual content with the real world with pixel-level accuracy.

Key challenges:
- **Dynamic lighting:** The virtual object must be lit to match the real environment (Spherical Harmonics, environment maps, neural relighting)
- **Occlusion:** A real object in front of a virtual one should hide it. Requires depth estimation or LiDAR
- **Latency:** Any delay between head movement and content update causes "swimming" of virtual objects; requires motion-to-photon latency <10 ms for see-through displays

**AR Display Types:**
| Type | Example | Principle |
|---|---|---|
| Video see-through | Meta Quest (passthrough mode) | Camera images + rendering composited on screen |
| Optical see-through | Microsoft HoloLens, Magic Leap | Transparent waveguides; virtual light added on top |
| Projection-based | Spatial AR installations | Projector maps onto real surfaces |
| Handheld | Smartphone AR | Camera + screen; no headset |

### 1.3.3 Key AR/VR Applications in Practice

**Medical:**
- Pre-surgical planning: overlay CT/MRI reconstructions onto the patient's body
- Navigation: real-time AR showing tumor boundaries during surgery (e.g., Augmedics xvision spine system)
- Training: VR surgical simulators (Touch Surgery, Osso VR)

**Education:**  
- Virtual anatomy labs; immersive historical reconstructions

**Industrial:**  
- AR assembly guidance overlaid on real machinery (Boeing, Airbus)
- VR safety training for hazardous environments

**Architecture & Construction:**  
- Walk through a building before it's built; AR overlay of BIM models on construction sites

**Entertainment & Gaming:**  
- Beat Saber, Half-Life: Alyx (VR); Pokémon GO, Ingress (AR)

## 1.4 Key Algorithms Underpinning AR/VR

| Algorithm | Purpose |
|---|---|
| SLAM (ORB-SLAM3, LSD-SLAM) | Map + localize |
| PnP (Perspective-n-Point) | Marker pose estimation |
| Kalman / Extended Kalman Filter | Sensor fusion (IMU + vision) |
| Depth Completion Networks | Dense depth from sparse LiDAR or monocular |
| NeRF (Neural Radiance Fields) | Photorealistic novel view synthesis |
| Gaussian Splatting (3DGS) | Real-time radiance field rendering |
| Lens Distortion Correction | Barrel/pincushion distortion of HMD optics |

---

# Chapter 2 — Geometric Modeling {#chapter-2}

Geometric modeling is the mathematical description and manipulation of 3D shapes. After acquiring 3D data (from LiDAR, photogrammetry, CT/MRI, etc.), we must process the raw data into clean, useful representations.

## 2.1 Point Clouds

### 2.1.1 What is a Point Cloud?

A **point cloud** is an unordered set of 3D points P = {p₁, p₂, ..., pₙ} where each point pᵢ = (xᵢ, yᵢ, zᵢ) represents a position in 3D space. Points may also carry additional attributes: color (R,G,B), surface normals, intensity (from LiDAR), or timestamps.

**Acquisition methods:**
- **LiDAR (Light Detection and Ranging):** A laser pulse is fired and the time-of-flight measured. Used in autonomous vehicles, surveying, and industrial scanning.
- **Structured Light Scanners:** Project a known light pattern (e.g., sinusoidal stripes); deformation of the pattern encodes depth (Intel RealSense D-series, Kinect)
- **Time-of-Flight Cameras:** Each pixel measures round-trip photon travel time (iToF, dToF)
- **Photogrammetry:** Multiple overlapping images are processed by Structure from Motion (SfM) algorithms to produce a dense point cloud
- **CT/MRI:** Medical scans provide 3D volumetric data that can be thresholded into point clouds

### 2.1.2 Point Cloud Data Structures

Efficient processing requires spatial data structures:

**k-d Tree:**  
A binary space-partitioning tree. Splits space alternately along x, y, z axes at median points. Supports O(log n) nearest-neighbor queries. Used extensively in ICP, normal estimation, and radius searches.

```
Build: choose axis with max variance → find median → recurse on left/right
Query: traverse tree, prune branches where minimum possible distance > current best
```

**Octree:**  
Recursively divides 3D space into 8 equal octants. Good for uniform density clouds; used for compression and level-of-detail.

**Voxel Grid:**  
Divides space into equal cubes (voxels). Points in each voxel are replaced by their centroid — a common downsampling strategy.

### 2.1.3 Normal Estimation

Normals are needed for rendering and surface reconstruction. For each point pᵢ:

1. Find k-nearest neighbors (k typically 10–30)
2. Compute the covariance matrix C of the neighbor coordinates
3. Perform PCA (eigendecomposition) on C
4. The normal is the eigenvector corresponding to the smallest eigenvalue (the direction of least variance)
5. Orient normals consistently (e.g., using minimum spanning tree or camera viewpoint)

## 2.2 Triangulation — Turning Points into Meshes

### 2.2.1 Why Triangulate?

A point cloud has no topology — we don't know which points are neighbors on the surface. Triangulation creates a **triangle mesh** (also called a **polygonal mesh** or **TIN — Triangulated Irregular Network**), which gives us:
- Continuous surface for rendering
- Well-defined surface normals per face
- Topology for further geometric processing

### 2.2.2 Delaunay Triangulation (2D)

**Definition:** Given a set of points P in the plane, the Delaunay triangulation DT(P) is the unique triangulation such that **no point in P lies inside the circumcircle of any triangle** in DT(P).

**Properties:**
- Maximizes the minimum angle among all triangles → avoids thin, degenerate "sliver" triangles
- Dual graph of the Voronoi diagram: connect circumcenters of adjacent triangles
- Unique in general position (no 4 co-circular points)
- For n points: O(n log n) time to compute; produces at most 2n − h − 2 triangles (h = convex hull points)

**Circumcircle condition (Delaunay condition):**  
For each edge shared by triangles T1 and T2: the fourth point of T2 must NOT lie inside the circumcircle of T1 (and vice versa). If it does, the shared edge is "flipped."

**Bowyer–Watson Algorithm:**
```
1. Start with a super-triangle containing all points
2. For each point p:
   a. Find all triangles whose circumcircle contains p  (bad triangles)
   b. Find the boundary polygon of the bad triangles (the "hole")
   c. Delete bad triangles; re-triangulate the hole with p as new vertex
3. Remove triangles sharing vertices with the super-triangle
```
Time complexity: O(n log n) average, O(n²) worst case.

**Lawson Flipping Algorithm:**  
Start with any valid triangulation; iteratively flip non-Delaunay edges until all edges satisfy the Delaunay condition. O(n²) in worst case but fast in practice.

### 2.2.3 3D Triangulation from Point Clouds

**Ball Pivoting Algorithm (BPA):**  
Imagine a ball of radius ρ rolling over the point cloud:
1. Seed: find three points that form a triangle and have the ball resting on them with no other point inside
2. Pivot: roll the ball around each edge; the next triangle vertex is the first point the ball touches
3. Continue until all points are reached or the ball gets stuck in a hole

The radius ρ determines the mesh resolution. Multiple passes with different ρ can recover fine and coarse features.

**Poisson Surface Reconstruction (Kazhdan et al., 2006):**  
One of the most widely used methods:
1. Estimate oriented point normals
2. Formulate surface reconstruction as solving a Poisson equation: ∇²χ = ∇·**V**, where **V** is the vector field of normals and χ is an indicator function (1 inside, 0 outside)
3. Extract the isosurface χ = 0.5 using Marching Cubes

Advantages: robust to noise, produces watertight closed meshes. Used in MeshLab, Open3D, PCL.

**Alpha Shapes:**  
A generalization of Delaunay triangulation. For a parameter α, delete all simplices (triangles, edges, vertices) whose circumradius exceeds 1/α. The result is a subset of the Delaunay triangulation that follows the shape of the point cloud.
- Large α → convex hull
- Small α → detailed concave shape, or potentially disconnected

**Marching Cubes Algorithm (Lorensen & Cline, 1987):**  
Used to extract an isosurface from a volumetric scalar field (e.g., CT voxels):
1. Divide space into small cubes
2. At each cube corner, evaluate whether the scalar value is above or below the iso-threshold
3. There are 2⁸ = 256 possible configurations (reduced to 15 by symmetry); each corresponds to a set of triangles within the cube
4. Interpolate edge intersection points; output triangles

This is the standard algorithm for medical image segmentation and volume rendering.

### 2.2.4 Summary Table: Triangulation Methods

| Method | Input | Output | Best For |
|---|---|---|---|
| Delaunay (2D) | 2D points | 2D triangles | Terrain, flat surfaces |
| Bowyer–Watson | 2D/3D points | Tetrahedral mesh (3D) | General purpose |
| Ball Pivoting | Oriented 3D points | Triangle mesh | Dense, clean scans |
| Poisson Reconstruction | Oriented 3D normals | Watertight mesh | Noisy data, medical |
| Alpha Shapes | 3D points | Concave hull mesh | Shape boundary extraction |
| Marching Cubes | Voxel grid | Isosurface mesh | CT/MRI volume data |

## 2.3 Mesh Simplification

### 2.3.1 Why Simplify?

Raw scans can contain millions of triangles. Simplification reduces the triangle count while preserving visual quality. This is essential for:
- Real-time rendering (games, VR)
- Level of Detail (LOD) systems
- Transmission over networks
- Faster downstream processing

### 2.3.2 Quadric Error Metrics (QEM) — Garland & Heckbert (1997)

The most widely used mesh simplification algorithm.

**Core Idea:** For each vertex, maintain a 4×4 symmetric matrix Q (the "quadric") that measures the squared distance from the vertex to the set of planes of its adjacent triangles. Collapsing an edge merges two vertices; the error of the collapse is the quadric error at the merged position.

**Algorithm:**
1. Compute Q matrix for every vertex (sum of outer products of plane equations of adjacent faces)
2. For each edge (v₁, v₂), compute optimal contracted position v̄ = argmin(v̄ᵀ Q_total v̄) and its error
3. Insert all edges into a min-heap ordered by error
4. Repeatedly extract the minimum-error edge and collapse it
5. Update Q matrices and edge costs for neighbors

**Error metric:**  
For a plane defined by ax + by + cz + d = 0 (with a² + b² + c² = 1), the squared distance from point **p** = [x,y,z,1]ᵀ is:

```
error(p) = pᵀ K p
where K = ppᵀ (outer product of the plane vector p = [a,b,c,d])
```

The vertex quadric Q = Σ K over all adjacent planes.

**Results:** Can reduce a 100,000 triangle mesh to 1,000 triangles with < 1% visual degradation if done carefully.

### 2.3.3 Other Simplification Methods

**Vertex Clustering:** Divide space into a grid; replace all vertices in each cell by a single representative. Fast but can create artifacts.

**Progressive Meshes (Hoppe, 1996):** Record each edge collapse as a reversible operation; store the original mesh as a sequence of "vertex splits." At runtime, apply the desired number of splits for adaptive LOD.

**View-Dependent Simplification:** Keep fine detail in regions close to the camera; use fewer triangles far away. Dynamically updates as the viewpoint changes.

## 2.4 Hole Filling and Surface Reconstruction

### 2.4.1 What are Holes?

Holes in a mesh arise from:
- Missing data during scanning (occluded regions, reflective surfaces, scanner limitations)
- Deliberate removal of corrupted regions
- Errors in reconstruction algorithms

A hole is a **boundary loop** in the mesh — a chain of boundary edges forming a closed polygon.

### 2.4.2 Simple Hole Filling Methods

**Ear Clipping / Triangulation of the Boundary Polygon:**  
1. Identify the boundary loop (ordered sequence of boundary vertices v₁, v₂, ..., vₙ)
2. Triangulate the polygon formed by these vertices
3. The simplest approach: connect each adjacent triple (vᵢ₋₁, vᵢ, vᵢ₊₁) creating "ears"

This produces a flat patch. For small holes, it is adequate.

**Minimum-Area Triangulation:**  
Among all possible triangulations of the boundary polygon, choose the one minimizing total triangle area. Can be computed in O(n³) using dynamic programming.

### 2.4.3 Feature-Preserving Hole Filling (Zhao et al., 2007)

For larger or more complex holes, the fill must match the surrounding surface curvature:

1. **Boundary analysis:** Detect curvature and normals along the hole boundary
2. **Initial fill:** Apply a rough triangulation to the hole
3. **Refinement:** Iteratively move interior vertices to minimize a fairness energy functional:

```
E = λ_fair × E_fairness + λ_fit × E_fit
```

where E_fairness penalizes high curvature (Laplacian smoothing) and E_fit attracts the patch toward known data.

**Laplacian smoothing step:**  
For each interior vertex v: v ← (1/|N|) Σ vᵢ over all neighbors N(v)  
Repeated application smooths the patch to match neighbors.

### 2.4.4 Poisson-Based Reconstruction for Holes

The same Poisson surface reconstruction (Section 2.2.3) can be applied to a partial mesh with holes:
1. Sample additional points around the hole boundary
2. Estimate their normals by interpolation from surrounding normals
3. Run full Poisson reconstruction on the combined point set
4. The algorithm naturally fills holes because it solves a global equation

### 2.4.5 Deep Learning Approaches

Recent methods use neural networks for hole filling:
- **PCN (Point Completion Network):** Takes incomplete point cloud; encoder-decoder outputs completed point cloud
- **FoldingNet, TopNet, PoinTr:** Various architectures for point cloud completion
- Used when the missing part can be inferred from context (e.g., the other half of a symmetric object)

## 2.5 Noise Removal and Point Set Regularization

### 2.5.1 Sources of Noise

- Scanner hardware limitations (quantization noise, sensor noise)
- Multi-path reflections (LiDAR bounces off multiple surfaces)
- Dust, humidity, vibration during scanning
- Registration errors when combining multiple scans

Noise manifests as:
- **Outliers:** Points far from the true surface (gross errors)
- **High-frequency noise:** Points near the surface but randomly scattered around it

### 2.5.2 Statistical Outlier Removal (SOR)

For each point pᵢ:
1. Find k nearest neighbors
2. Compute mean distance μᵢ and standard deviation σᵢ of distances to neighbors
3. Compute global mean μ and standard deviation σ across all points
4. Remove point if μᵢ > μ + α·σ (where α is a threshold, typically 1.0–2.0)

This removes isolated points that are far from their neighborhood.

### 2.5.3 Radius Outlier Removal

Remove points that have fewer than N neighbors within a radius r. Very fast; removes isolated points in sparse regions.

### 2.5.4 Bilateral Filtering for Point Clouds

Adapted from image processing. For each point pᵢ, compute a new position p'ᵢ as a weighted average of neighbors:

```
p'ᵢ = Σⱼ w(pᵢ, pⱼ) · pⱼ  /  Σⱼ w(pᵢ, pⱼ)

w(pᵢ, pⱼ) = exp(−||pᵢ−pⱼ||² / σ²_spatial) · exp(−||nᵢ·(pᵢ−pⱼ)||² / σ²_normal)
```

The first term uses spatial proximity; the second uses projected distance along the normal direction (preserving edges and sharp features). σ values control the smoothing strength.

### 2.5.5 Moving Least Squares (MLS)

The MLS method fits a local polynomial surface to the neighborhood of each point and projects the point onto that surface:

1. For each point pᵢ, gather k-nearest neighbors
2. Fit a local plane or low-degree polynomial p(u,v) to those neighbors by least-squares, with Gaussian weights centered at pᵢ
3. Project pᵢ onto the fitted surface
4. Recompute normals from the surface fit

MLS both smooths and regularizes — moving noisy points onto a smooth implicit surface. It is the basis of the **APSS (Algebraic Point Set Surfaces)** method.

### 2.5.6 Voxel Downsampling (Regularization)

To make a point set "more regular" (uniform density):
1. Create a 3D voxel grid of cell size `leaf_size`
2. All points in each voxel cell are replaced by their centroid
3. Result: one point per non-empty voxel → uniform density

Fast O(n log n) implementation in PCL (Point Cloud Library) and Open3D.

### 2.5.7 Comparison of Denoising Methods

| Method | Removes Outliers | Smooths Noise | Preserves Sharp Edges | Speed |
|---|---|---|---|---|
| Statistical Outlier Removal | ✓ | ✗ | ✓ | Fast |
| Radius Outlier Removal | ✓ | ✗ | ✓ | Very Fast |
| Voxel Downsampling | Partial | Partial | ✗ | Very Fast |
| Bilateral Filtering | ✗ | ✓ | ✓ | Moderate |
| MLS | ✗ | ✓ | ✓ | Slow |

---

# Chapter 3 — Medical Image Processing {#chapter-3}

## 3.1 CT Scanning (Computed Tomography)

### 3.1.1 Physical Principle

CT uses **X-rays** — ionizing electromagnetic radiation. A rotating X-ray source and detector array around the patient take hundreds of 2D projection images (sinograms) from different angles. A mathematical procedure called **back-projection** (specifically **filtered back-projection**, FBP) reconstructs the 3D density distribution.

**Hounsfield Units (HU):**  
The attenuation of X-rays by tissue is expressed in Hounsfield Units:

| Tissue | HU Value |
|---|---|
| Air | −1000 |
| Lung | −500 to −700 |
| Fat | −100 to −50 |
| Water | 0 |
| Soft tissue | +20 to +80 |
| Bone | +300 to +1900 |

This allows **windowing** — adjusting contrast and brightness to highlight specific tissue types.

### 3.1.2 CT Reconstruction Algorithm — Filtered Back-Projection

1. **Projection acquisition:** For each angle θ, measure the line integral of X-ray attenuation along every ray through the object → produces the **Radon transform** Rθ(s)

2. **Filtering step:** Apply a ramp filter (Ram-Lak filter) in the frequency domain to each projection:  
   `H(f) = |f|` (enhances high frequencies, counteracts blurring from back-projection)

3. **Back-projection:** For each filtered projection, smear the values back along the ray paths and sum up:  
   `f(x,y) = ∫₀^π P_θ(x cosθ + y sinθ) dθ`

4. **Result:** A 3D voxel grid showing tissue density.

**Iterative reconstruction (IR):** Modern CT scanners use iterative methods (ASIR, IRIS, SAFIRE) that model noise statistics and scanner physics, allowing lower radiation doses with comparable image quality.

### 3.1.3 CT Advantages and Disadvantages

**Advantages:**
- Excellent for bone, calcifications, lung
- Fast acquisition (entire chest in one breath-hold)
- Wide availability
- Precise HU values enable automated segmentation

**Disadvantages:**
- Ionizing radiation (cumulative dose risk)
- Poor soft-tissue contrast (compared to MRI)
- Artifacts: beam hardening, metal artifacts, partial volume effect

## 3.2 MRI Scanning (Magnetic Resonance Imaging)

### 3.2.1 Physical Principle

MRI exploits the **nuclear magnetic resonance (NMR)** of hydrogen nuclei (protons).

1. **Alignment:** A strong static magnetic field B₀ (1.5T, 3T, or 7T) aligns proton spins parallel or anti-parallel to the field

2. **Excitation:** A radiofrequency (RF) pulse at the Larmor frequency  
   `f_L = γ B₀ / (2π)`  
   (γ = 42.577 MHz/T for hydrogen) tips the net magnetization into the transverse plane

3. **Relaxation:** After the RF pulse, two relaxation processes occur:
   - **T1 (longitudinal relaxation):** Magnetization recovers along B₀; different tissues have different T1 times
   - **T2 (transverse relaxation):** Transverse magnetization decays due to spin-spin interactions; also tissue-specific

4. **Signal detection:** The relaxing magnetization induces a voltage in receiver coils — the **FID (Free Induction Decay)** signal

5. **Spatial encoding:** Gradient coils create spatially varying magnetic fields. The frequency and phase of the signal encode position. **2D Fourier transform** of the collected k-space data produces the image.

### 3.2.2 MRI Sequences and Weighting

By choosing the **Repetition Time (TR)** and **Echo Time (TE)**, different tissue contrasts are achieved:

| Sequence | TR | TE | Bright | Uses |
|---|---|---|---|---|
| T1-weighted | Short | Short | Fat, contrast-enhancing lesions | Anatomy, post-contrast brain |
| T2-weighted | Long | Long | Fluid, edema, CSF | Pathology detection, brain |
| PD-weighted | Long | Short | Proton density | Cartilage, joint imaging |
| FLAIR | Long | Long (fluid suppressed) | White matter lesions | MS, encephalitis |
| DWI (diffusion) | — | — | Restricted diffusion (ischemia) | Stroke, tumor cellularity |
| fMRI (BOLD) | — | — | Blood oxygenation | Brain activity mapping |

### 3.2.3 MRI Advantages and Disadvantages

**Advantages:**
- No ionizing radiation
- Excellent soft-tissue contrast (brain, spinal cord, joint cartilage, liver)
- Multi-parametric: T1, T2, DWI, perfusion, spectroscopy in one session
- Functional imaging possible (fMRI, DTI)

**Disadvantages:**
- Long acquisition time (minutes vs. seconds for CT)
- Loud noise (gradient switching)
- Contraindicated in patients with certain metal implants (pacemakers, some stents)
- Expensive, less widely available
- Susceptibility to motion artifacts
- Limited spatial resolution for some applications

## 3.3 3D Reconstruction from Medical Scans

### 3.3.1 Workflow Overview

```
CT/MRI Acquisition
        ↓
DICOM Data (stack of 2D slices, e.g., 512×512 × 300 slices)
        ↓
Segmentation (which voxels belong to the target structure?)
        ↓
3D Surface Extraction (Marching Cubes)
        ↓
Mesh Post-Processing (smoothing, hole filling, simplification)
        ↓
Visualization / 3D Printing / Surgical Planning
```

### 3.3.2 Segmentation Methods

**Thresholding:**  
For bone: any voxel with HU > 300 is classified as bone. Fast and effective for high-contrast structures (CT bone, lung).

**Region Growing:**  
1. Place a seed point inside the target organ
2. Recursively add adjacent voxels if their intensity is within a tolerance range
3. Stops at edges (abrupt intensity changes)

**Watershed Segmentation:**  
Treat the image as a topographic map; flood from local minima; watershed lines separate different regions. Good for touching structures.

**Active Contours (Snakes, Level Sets):**  
Evolve a curve/surface toward object boundaries by minimizing an energy:

```
E = E_internal (smoothness) + E_external (image gradient)
```

Level set methods represent the surface implicitly as the zero-level of a function φ(x,y,z), which evolves according to:

```
∂φ/∂t = |∇φ| (κ + F)
```

where κ is curvature and F is the image-based speed term.

**Deep Learning Segmentation:**  
- **U-Net (Ronneberger et al., 2015):** The dominant architecture for medical image segmentation
  - Encoder path: consecutive conv + max-pool (extracts features, increases receptive field)
  - Bottleneck: lowest resolution
  - Decoder path: upsampling + skip connections from encoder (restores spatial detail)
  - Output: pixel-wise probability map
- **3D U-Net:** Extends to volumetric segmentation
- **nnU-Net:** Self-configuring framework that adapts to any segmentation dataset automatically

### 3.3.3 Marching Cubes Applied to Medical Data

After segmentation, the binary volume is passed to Marching Cubes:
1. Each 2×2×2 voxel cube has 8 corners classified as inside/outside the object
2. 256 configurations → 15 unique cases by symmetry
3. Each case defines which edges are intersected and how to place triangles
4. Linear interpolation finds precise edge intersection positions

**Post-processing the medical mesh:**
- **Laplacian smoothing:** reduces staircase artifacts from the voxel grid
- **Taubin smoothing (λ-μ filter):** smooths without shrinkage (alternating positive/negative smoothing steps)
- **Mesh simplification:** reduce triangle count while maintaining shape
- **Hole filling:** fill any topological holes in the mesh

## 3.4 Brain Tumor Detection

### 3.4.1 Types of Brain Tumors in MRI

**Primary tumors (originating in the brain):**
- Glioblastoma Multiforme (GBM) — Grade IV, most aggressive; heterogeneous enhancement on T1c; central necrosis
- Low-grade glioma — Grades II–III; T2/FLAIR hyperintense; minimal enhancement
- Meningioma — Extra-axial; strong enhancement on T1c
- Medulloblastoma — Posterior fossa; pediatric

**Secondary (metastatic):**  
- Ring-enhancing lesions on T1c; often multiple; surrounded by vasogenic edema (T2/FLAIR bright)

### 3.4.2 MRI Sequences for Brain Tumor Diagnosis

The standard **multi-parametric MRI (mpMRI)** protocol for brain tumors includes:
- **T1 (pre-contrast):** Baseline anatomy; hemorrhage appears bright
- **T1c (post-gadolinium contrast):** Blood-brain barrier breakdown shows enhancement; tumor core
- **T2:** Peritumoral edema bright; shows tumor extent
- **T2-FLAIR:** Fluid suppressed; edema and infiltration clearly visible
- **DWI/ADC:** Cell density; tumor cellularity; differentiates abscess from tumor
- **MR Spectroscopy (MRS):** Choline↑ (cell membrane turnover), NAA↓ (neuronal death); Cho/Cr and Cho/NAA ratios indicate malignancy
- **Perfusion MRI (DSC, DCE):** Blood volume and flow; rCBV elevated in high-grade tumor

### 3.4.3 Manual vs. Automated Segmentation

**Manual segmentation:** Radiologist draws tumor boundaries on each slice — gold standard but time-consuming (1–4 hours per case) and subject to inter-rater variability.

**BraTS (Brain Tumor Segmentation) Challenge:**  
An annual competition (MICCAI) providing a standardized dataset and evaluation for automated tumor segmentation. Sub-regions:
- **Enhancing tumor (ET):** T1c-bright region (active tumor)
- **Tumor core (TC):** ET + necrosis
- **Whole tumor (WT):** TC + peritumoral edema

### 3.4.4 Deep Learning for Brain Tumor Segmentation

**3D U-Net / U-Net variants:**  
The current state of the art. Input: 4-channel volume (T1, T1c, T2, FLAIR). Output: 3-channel probability map (ET, TC, WT regions).

**Attention U-Net:**  
Adds attention gates on skip connections to focus on relevant regions; suppresses irrelevant background activations.

**Transformer-based models:**  
- **Swin-UNet, TransBTS, nnFormer:** Use self-attention to capture long-range dependencies (important for irregular tumor shapes)

**Training considerations:**
- Class imbalance: tumor voxels ≈ 1–2% of total; use weighted loss, focal loss, or oversampling
- Loss functions: Dice loss + cross-entropy (combined) is standard
- Data augmentation: random flipping, rotation, intensity scaling, elastic deformation, Gaussian noise

### 3.4.5 Performance Metrics for Tumor Segmentation

**Dice Similarity Coefficient (DSC):**
```
DSC = 2 |A ∩ B| / (|A| + |B|)
```
where A = predicted region, B = ground truth. Range [0,1]; 1 = perfect overlap.  
State-of-the-art BraTS results: DSC ≈ 0.88–0.92 for whole tumor.

**Hausdorff Distance (HD95):**  
The 95th percentile of distances between surface points of predicted and ground truth meshes. Measures worst-case boundary localization error.

**Sensitivity / Specificity:**
- Sensitivity (Recall) = TP / (TP + FN) — how many true tumor voxels are found
- Specificity = TN / (TN + FP) — how many non-tumor voxels are correctly excluded

### 3.4.6 Clinical Application Pipeline

```
Patient presents with symptoms (headache, seizures, focal deficits)
           ↓
Multi-parametric MRI acquisition
           ↓
AI-assisted segmentation (U-Net or similar) → approximate tumor boundaries
           ↓
Radiologist review and correction (human-in-the-loop)
           ↓
3D tumor volume rendered for surgical planning
           ↓
Optional: tractography (DTI) to map fiber tracts near tumor
           ↓
Surgical resection with AR navigation overlay
           ↓
Post-operative MRI to assess residual tumor
           ↓
Radiation therapy planning (tumor + margin outlined)
```

---

# Chapter 4 — Curves and Surfaces: The Key Math {#chapter-4}

> **Exam-Critical:** The professor explicitly said: "Focus on the three formulas: Bézier Curve, Bézier Surface, and De Casteljau Algorithm." This chapter covers all three in full detail with worked examples.

## 4.1 Bézier Curves

### 4.1.1 History and Context

The Bézier curve is named after **Pierre Bézier** (1910–1999), a French engineer at Renault, who used them in the 1960s for designing car body shapes. The mathematical basis — **Bernstein polynomials** — was established earlier by Sergei Bernstein in 1912. **Paul de Casteljau** independently developed his algorithm at Citroën in 1959, which remained a trade secret until the 1980s.

Today, Bézier curves are used in:
- Font design (PostScript, TrueType, OpenType)
- Vector graphics (Adobe Illustrator "paths", SVG)
- CAD/CAM (NURBS are generalizations)
- Animation (ease-in / ease-out timing)
- Robotics (smooth trajectory planning)

### 4.1.2 Control Points and the Curve

A Bézier curve of **degree n** is defined by **n+1 control points** P₀, P₁, ..., Pₙ.

The curve B(t) traces a path for t ∈ [0, 1]:
- B(0) = P₀ (the curve always starts at the first control point)
- B(1) = Pₙ (the curve always ends at the last control point)
- Intermediate control points "attract" but don't lie on the curve (in general)

### 4.1.3 Bernstein Polynomial Form

**Bernstein basis polynomial of degree n:**
```
Bᵢ,ₙ(t) = C(n,i) · tⁱ · (1−t)^(n−i)
```

where C(n,i) = n! / (i! (n−i)!) is the binomial coefficient.

**Bézier curve formula:**
```
B(t) = Σᵢ₌₀ⁿ Bᵢ,ₙ(t) · Pᵢ
     = Σᵢ₌₀ⁿ C(n,i) · tⁱ · (1−t)^(n−i) · Pᵢ
```

### 4.1.4 Cases by Degree

**Linear (n=1) — 2 control points:**
```
B(t) = (1−t)P₀ + tP₁
```
This is simple linear interpolation. The curve is a straight line segment.

---

**Quadratic (n=2) — 3 control points:**
```
B(t) = (1−t)²P₀ + 2(1−t)tP₁ + t²P₂
```

Bernstein weights: (1−t)², 2t(1−t), t²  
These sum to 1: [(1−t) + t]² = 1 ✓

The curve passes through P₀ and P₂, and is "pulled toward" P₁.

---

**Cubic (n=3) — 4 control points:**
```
B(t) = (1−t)³P₀ + 3(1−t)²tP₁ + 3(1−t)t²P₂ + t³P₃
```

Bernstein weights: (1−t)³, 3(1−t)²t, 3(1−t)t², t³  
These sum to 1: [(1−t) + t]³ = 1 ✓

Cubic Bézier curves are the most common in practice (Adobe Illustrator, font outlines, CSS animations).

---

**General (arbitrary n):**  
The binomial coefficients for the first several degrees:

| Degree | Coefficients | Formula |
|---|---|---|
| 1 | 1 1 | (1−t) t |
| 2 | 1 2 1 | (1−t)² 2(1−t)t t² |
| 3 | 1 3 3 1 | (1−t)³ 3(1−t)²t 3(1−t)t² t³ |
| 4 | 1 4 6 4 1 | (1−t)⁴ ... t⁴ |
| 5 | 1 5 10 10 5 1 | (1−t)⁵ ... t⁵ |

(Pascal's triangle gives the binomial coefficients)

### 4.1.5 Properties of Bézier Curves

| Property | Description |
|---|---|
| Endpoint interpolation | B(0) = P₀, B(1) = Pₙ |
| Convex hull property | Entire curve lies within convex hull of control points |
| Affine invariance | Transform control points → same as transforming curve |
| Tangent at endpoints | B'(0) = n(P₁−P₀); B'(1) = n(Pₙ−Pₙ₋₁) |
| Variation diminishing | Curve crosses any line no more times than the control polygon does |
| Symmetry | Reversing control point order gives the same curve reversed |

**Tangent at t=0:**  
B'(0) = n(P₁ − P₀) — the curve is tangent to the first edge of the control polygon

**Tangent at t=1:**  
B'(1) = n(Pₙ − Pₙ₋₁) — the curve is tangent to the last edge

These properties enable **C1 continuity** between two Bézier segments if you align P₂, Pₙ, and Q₁ (first control point of next curve) collinearly: Pₙ − Pₙ₋₁ = Q₁ − Q₀.

### 4.1.6 Derivative Formula

The first derivative of a degree-n Bézier curve is a degree-(n-1) Bézier curve:
```
B'(t) = n · Σᵢ₌₀^(n−1) Bᵢ,ₙ₋₁(t) · (Pᵢ₊₁ − Pᵢ)
```

The second derivative:
```
B''(t) = n(n-1) · Σᵢ₌₀^(n−2) Bᵢ,ₙ₋₂(t) · (Pᵢ₊₂ − 2Pᵢ₊₁ + Pᵢ)
```

### 4.1.7 Composite Bézier Curves (Splines)

A single high-degree curve is hard to control. In practice, multiple cubic segments are joined:

- **C0 continuity:** Endpoint of curve i = start of curve i+1 (no gap)
- **C1 continuity:** Equal first derivatives (tangent direction AND magnitude match)
- **G1 continuity:** Equal tangent direction only (not magnitude); visually smooth junction
- **C2 continuity:** Equal second derivatives (curvature matches); smoother but more constrained

## 4.2 Bézier Surfaces

### 4.2.1 Extension to 2D Parameter Space

A Bézier surface of degree (m, n) is defined by a **(m+1) × (n+1) grid of control points** Pᵢ,ⱼ.

It maps two parameters (u, v) ∈ [0,1]² to a 3D point:

```
B(u,v) = Σᵢ₌₀ᵐ Σⱼ₌₀ⁿ Bᵢ,ₘ(u) · Bⱼ,ₙ(v) · Pᵢ,ⱼ
```

where Bᵢ,ₘ(u) is the Bernstein basis in u-direction, and Bⱼ,ₙ(v) is the Bernstein basis in v-direction.

**Interpretation:** Fix u → you get a Bézier curve in v-direction with control points Qⱼ(u) = Σᵢ Bᵢ,ₘ(u) Pᵢ,ⱼ. Varying v traces a Bézier curve through those moving control points.

### 4.2.2 Bicubic Bézier Patch (Most Common)

Degree (3,3): 4×4 = **16 control points**, parameters (u, v) ∈ [0,1]²

```
B(u,v) = Σᵢ₌₀³ Σⱼ₌₀³ B_{i,3}(u) · B_{j,3}(v) · P_{i,j}
```

Written in matrix form:
```
B(u,v) = U · M · P · Mᵀ · Vᵀ
```

where:
- U = [u³, u², u, 1]
- V = [v³, v², v, 1]
- M is the 4×4 Bézier basis matrix:
```
M = [ -1  3 -3  1 ]
    [  3 -6  3  0 ]
    [ -3  3  0  0 ]
    [  1  0  0  0 ]
```
- P is the 4×4×3 control point matrix

### 4.2.3 Properties

All properties of Bézier curves extend to surfaces:
- **Endpoint interpolation:** B(0,0) = P₀,₀ etc. (corner points are on the surface)
- **Edge curves:** B(0,v) is a Bézier curve through control points P₀,₀, P₀,₁, P₀,₂, P₀,₃
- **Convex hull:** Surface lies within convex hull of control points
- **Partial derivatives (tangent planes):**  
  ∂B/∂u(0,0) = 3(P₁,₀ − P₀,₀) — tangent in u-direction at corner  
  ∂B/∂v(0,0) = 3(P₀,₁ − P₀,₀) — tangent in v-direction at corner  
  Normal = (∂B/∂u) × (∂B/∂v)

### 4.2.4 Evaluating a Point on the Surface

**Method:** Apply De Casteljau in u-direction to get intermediate control points, then apply De Casteljau in v-direction (or vice versa).

**Algorithm:**
1. Fix u₀. For each row i (i = 0..m), evaluate the Bézier curve Qᵢ(u₀) = De Casteljau on row i at parameter u₀. This gives (n+1) intermediate points {Q₀, Q₁, ..., Qₙ}.
2. Fix v₀. Apply De Casteljau on {Q₀, ..., Qₙ} at parameter v₀. The result is B(u₀, v₀).

## 4.3 De Casteljau's Algorithm

### 4.3.1 Motivation

While the Bernstein polynomial formula is mathematically clean, direct evaluation requires computing large binomial coefficients (e.g., C(20,10) = 184,756 for a degree-20 curve) and is numerically unstable for high degrees.

De Casteljau's algorithm avoids these issues:
- No large numbers
- Numerically stable (each step is just a linear interpolation)
- Also provides curve subdivision as a byproduct

### 4.3.2 The Algorithm

Given control points P₀, P₁, ..., Pₙ and parameter t₀ ∈ [0,1]:

**Initialize:** Set Pᵢ⁽⁰⁾ = Pᵢ for i = 0, 1, ..., n

**Recurrence relation:**
```
Pᵢ⁽ʲ⁾ = (1 − t₀) · Pᵢ⁽ʲ⁻¹⁾ + t₀ · Pᵢ₊₁⁽ʲ⁻¹⁾
```

for j = 1, 2, ..., n and i = 0, 1, ..., n−j

**Result:** B(t₀) = P₀⁽ⁿ⁾

Each step linearly interpolates between adjacent points with ratio t₀. After n rounds, one point remains — that is the curve point.

### 4.3.3 Triangular Scheme (Hand Calculation Table)

The computation can be organized in a triangular table:

```
j=0        j=1          j=2          j=3 (result)
P₀⁽⁰⁾
          P₀⁽¹⁾
P₁⁽⁰⁾              P₀⁽²⁾
          P₁⁽¹⁾                P₀⁽³⁾ ← Answer
P₂⁽⁰⁾              P₁⁽²⁾
          P₂⁽¹⁾
P₃⁽⁰⁾
```

Each entry is the linear interpolation of its two upper-left neighbors.

### 4.3.4 Geometric Interpretation

Each iteration shrinks the polygon by linear interpolation. The intermediate points at each level form a new control polygon. The key insight:

- At parameter t₀, the leftmost column of the triangular table {P₀⁽⁰⁾, P₀⁽¹⁾, ..., P₀⁽ⁿ⁾} gives control points for the LEFT sub-curve B₁(t) for t ∈ [0, t₀]
- The diagonal {P₀⁽ⁿ⁾, P₁⁽ⁿ⁻¹⁾, ..., Pₙ⁽⁰⁾} gives control points for the RIGHT sub-curve B₂(t) for t ∈ [t₀, 1]

This is **curve subdivision** — splitting one curve into two Bézier curves at any parameter value.

### 4.3.5 Pseudocode

```python
def de_casteljau(points, t):
    """
    points: list of control points [[x0,y0], [x1,y1], ..., [xn,yn]]
    t: parameter in [0,1]
    returns: point on curve at parameter t
    """
    p = [list(pt) for pt in points]  # copy
    n = len(p) - 1
    for j in range(1, n + 1):
        for i in range(n - j + 1):
            p[i][0] = (1 - t) * p[i][0] + t * p[i+1][0]
            p[i][1] = (1 - t) * p[i][1] + t * p[i+1][1]
    return p[0]
```

### 4.3.6 Complexity

- For a degree-n curve: n + (n−1) + ... + 1 = n(n+1)/2 linear interpolations
- Each linear interpolation is O(1) operations per coordinate
- Total: O(n²) per evaluation
- Compared to direct Bernstein: also O(n²) but with better numerical properties

## 4.4 Worked Computation Examples

> These are the types of computation questions expected in the exam.

### Example 1: Quadratic Bézier Curve at t = 0.75

**Given:** Control points P₀ = (0, 0), P₁ = (1, 2), P₂ = (3, 0)  
**Find:** B(0.75)

**Method A: Bernstein Formula**
```
B(t) = (1−t)²·P₀ + 2t(1−t)·P₁ + t²·P₂

At t = 0.75:
  (1−0.75)² = 0.25² = 0.0625
  2·0.75·0.25 = 0.375
  0.75² = 0.5625

B(0.75) = 0.0625·(0,0) + 0.375·(1,2) + 0.5625·(3,0)
x = 0 + 0.375 + 1.6875 = 2.0625
y = 0 + 0.75 + 0 = 0.75

Answer: B(0.75) = (2.0625, 0.75)
```

**Method B: De Casteljau**
```
Level 0:  P₀=(0,0)  P₁=(1,2)  P₂=(3,0)

Level 1 (linear interp with t=0.75):
  P₀¹ = (1−0.75)·(0,0) + 0.75·(1,2)
       = 0.25·(0,0) + 0.75·(1,2)
       = (0,0) + (0.75, 1.5) = (0.75, 1.5)

  P₁¹ = (1−0.75)·(1,2) + 0.75·(3,0)
       = 0.25·(1,2) + 0.75·(3,0)
       = (0.25, 0.5) + (2.25, 0) = (2.5, 0.5)

Level 2 (final, t=0.75):
  P₀² = (1−0.75)·(0.75, 1.5) + 0.75·(2.5, 0.5)
       = 0.25·(0.75,1.5) + 0.75·(2.5,0.5)
       = (0.1875, 0.375) + (1.875, 0.375)
       = (2.0625, 0.75)

Answer: B(0.75) = (2.0625, 0.75) ✓
```

---

### Example 2: Cubic Bézier Curve at t = 0.5

**Given:** P₀ = (0,0), P₁ = (0,1), P₂ = (1,1), P₃ = (1,0)  
**Find:** B(0.5)

**De Casteljau at t = 0.5:**

```
Level 0:
  P₀⁰ = (0,0)
  P₁⁰ = (0,1)
  P₂⁰ = (1,1)
  P₃⁰ = (1,0)

Level 1 [Pᵢ¹ = 0.5·Pᵢ + 0.5·Pᵢ₊₁]:
  P₀¹ = 0.5·(0,0) + 0.5·(0,1) = (0, 0.5)
  P₁¹ = 0.5·(0,1) + 0.5·(1,1) = (0.5, 1)
  P₂¹ = 0.5·(1,1) + 0.5·(1,0) = (1, 0.5)

Level 2 [Pᵢ² = 0.5·Pᵢ¹ + 0.5·Pᵢ₊₁¹]:
  P₀² = 0.5·(0,0.5) + 0.5·(0.5,1) = (0.25, 0.75)
  P₁² = 0.5·(0.5,1) + 0.5·(1,0.5) = (0.75, 0.75)

Level 3 [final]:
  P₀³ = 0.5·(0.25,0.75) + 0.5·(0.75,0.75) = (0.5, 0.75)

Answer: B(0.5) = (0.5, 0.75)
```

---

### Example 3: Cubic Bézier at t = 3/4 (the professor's example)

**Given:** Six points P₀=(0,0), P₁=(1,0), P₂=(2,1), P₃=(3,1), P₄=(4,0), P₅=(5,0)  
(This is a **degree-5** curve — 6 points)  
**Find:** B(0.75) using De Casteljau

**De Casteljau at t = 0.75:**

```
Level 0 (j=0):
  P₀ = (0,0)
  P₁ = (1,0)
  P₂ = (2,1)
  P₃ = (3,1)
  P₄ = (4,0)
  P₅ = (5,0)

Level 1 (j=1), lerp with t=0.75:
  Q₀ = 0.25·(0,0) + 0.75·(1,0)   = (0.75, 0)
  Q₁ = 0.25·(1,0) + 0.75·(2,1)   = (1.75, 0.75)
  Q₂ = 0.25·(2,1) + 0.75·(3,1)   = (2.75, 1)
  Q₃ = 0.25·(3,1) + 0.75·(4,0)   = (3.75, 0.25)
  Q₄ = 0.25·(4,0) + 0.75·(5,0)   = (4.75, 0)

Level 2 (j=2):
  R₀ = 0.25·(0.75,0)   + 0.75·(1.75,0.75) = (0.1875+1.3125, 0+0.5625) = (1.5, 0.5625)
  R₁ = 0.25·(1.75,0.75)+ 0.75·(2.75,1)   = (0.4375+2.0625, 0.1875+0.75) = (2.5, 0.9375)
  R₂ = 0.25·(2.75,1)  + 0.75·(3.75,0.25) = (0.6875+2.8125, 0.25+0.1875) = (3.5, 0.4375)
  R₃ = 0.25·(3.75,0.25)+ 0.75·(4.75,0)  = (0.9375+3.5625, 0.0625+0)   = (4.5, 0.0625)

Level 3 (j=3):
  S₀ = 0.25·(1.5,0.5625) + 0.75·(2.5,0.9375) = (0.375+1.875, 0.140625+0.703125) = (2.25, 0.84375)
  S₁ = 0.25·(2.5,0.9375) + 0.75·(3.5,0.4375) = (0.625+2.625, 0.234375+0.328125) = (3.25, 0.5625)
  S₂ = 0.25·(3.5,0.4375) + 0.75·(4.5,0.0625) = (0.875+3.375, 0.109375+0.046875) = (4.25, 0.15625)

Level 4 (j=4):
  T₀ = 0.25·(2.25,0.84375) + 0.75·(3.25,0.5625)
     = (0.5625+2.4375, 0.2109375+0.421875) = (3.0, 0.6328125)
  T₁ = 0.25·(3.25,0.5625) + 0.75·(4.25,0.15625)
     = (0.8125+3.1875, 0.140625+0.1171875) = (4.0, 0.2578125)

Level 5 (j=5, final):
  U₀ = 0.25·(3.0,0.6328125) + 0.75·(4.0,0.2578125)
     = (0.75+3.0, 0.158203125+0.193359375) = (3.75, 0.35156...)

Answer: B(0.75) ≈ (3.75, 0.352)
```

---

### Example 4: Bézier Surface Point

**Given:** A degree-(2,2) Bézier patch with control grid (3×3 = 9 points):
```
P₀,₀=(0,0,0)  P₀,₁=(1,0,1)  P₀,₂=(2,0,0)
P₁,₀=(0,1,1)  P₁,₁=(1,1,2)  P₁,₂=(2,1,1)
P₂,₀=(0,2,0)  P₂,₁=(1,2,1)  P₂,₂=(2,2,0)
```
**Find:** B(0.5, 0.5)

**Step 1:** For each row i, evaluate quadratic Bézier in v at v=0.5:

Row i=0: P₀,₀, P₀,₁, P₀,₂ at v=0.5
```
Q₀ = (1−0.5)²·(0,0,0) + 2·0.5·0.5·(1,0,1) + 0.5²·(2,0,0)
   = 0.25·(0,0,0) + 0.5·(1,0,1) + 0.25·(2,0,0)
   = (0,0,0) + (0.5,0,0.5) + (0.5,0,0) = (1.0, 0.0, 0.5)
```

Row i=1: P₁,₀, P₁,₁, P₁,₂ at v=0.5
```
Q₁ = 0.25·(0,1,1) + 0.5·(1,1,2) + 0.25·(2,1,1)
   = (0,0.25,0.25) + (0.5,0.5,1) + (0.5,0.25,0.25) = (1.0, 1.0, 1.5)
```

Row i=2: P₂,₀, P₂,₁, P₂,₂ at v=0.5
```
Q₂ = 0.25·(0,2,0) + 0.5·(1,2,1) + 0.25·(2,2,0)
   = (0,0.5,0) + (0.5,1,0.5) + (0.5,0.5,0) = (1.0, 2.0, 0.5)
```

**Step 2:** Evaluate quadratic Bézier in u at u=0.5 through {Q₀, Q₁, Q₂}:
```
B(0.5,0.5) = 0.25·Q₀ + 0.5·Q₁ + 0.25·Q₂
           = 0.25·(1,0,0.5) + 0.5·(1,1,1.5) + 0.25·(1,2,0.5)
           = (0.25,0,0.125) + (0.5,0.5,0.75) + (0.25,0.5,0.125)
           = (1.0, 1.0, 1.0)

Answer: B(0.5, 0.5) = (1, 1, 1)
```

---

### Example 5: Curve Tangent Vectors

**Given:** Cubic Bézier with P₀=(0,0), P₁=(1,3), P₂=(2,3), P₃=(3,0)

**Tangent at t=0:**
```
B'(0) = n·(P₁ − P₀) = 3·((1,3)−(0,0)) = 3·(1,3) = (3, 9)
```
Direction: from (0,0) toward (1,3), scaled by 3.

**Tangent at t=1:**
```
B'(1) = n·(Pₙ − Pₙ₋₁) = 3·((3,0)−(2,3)) = 3·(1,−3) = (3, −9)
```
Direction: from (2,3) toward (3,0), scaled by 3.

---

### Summary Formula Sheet

**Linear Bézier (n=1):**
```
B(t) = (1−t)P₀ + tP₁
```

**Quadratic Bézier (n=2):**
```
B(t) = (1−t)²P₀ + 2t(1−t)P₁ + t²P₂
```

**Cubic Bézier (n=3):**
```
B(t) = (1−t)³P₀ + 3t(1−t)²P₁ + 3t²(1−t)P₂ + t³P₃
```

**General Bézier (degree n):**
```
B(t) = Σᵢ₌₀ⁿ C(n,i) · tⁱ · (1−t)^(n−i) · Pᵢ
```

**Bézier Surface (degree m×n):**
```
B(u,v) = Σᵢ₌₀ᵐ Σⱼ₌₀ⁿ C(m,i)·uⁱ·(1−u)^(m−i) · C(n,j)·vʲ·(1−v)^(n−j) · Pᵢ,ⱼ
```

**De Casteljau Recurrence:**
```
Pᵢ⁽⁰⁾ = Pᵢ  (initial)
Pᵢ⁽ʲ⁾ = (1−t)·Pᵢ⁽ʲ⁻¹⁾ + t·Pᵢ₊₁⁽ʲ⁻¹⁾  (recurrence)
B(t) = P₀⁽ⁿ⁾  (result)
```

**Tangents:**
```
B'(0) = n·(P₁ − P₀)
B'(1) = n·(Pₙ − Pₙ₋₁)
```

---

# Appendix A — Quick Reference: Algorithms Summary

| Topic | Algorithm | Key Idea |
|---|---|---|
| VR Tracking | SLAM + IMU Kalman fusion | Map + localize simultaneously |
| AR Tracking | PnP (marker) or SLAM (markerless) | Camera pose from known points |
| Triangulation 2D | Delaunay / Bowyer-Watson | Maximize min angle; circumcircle condition |
| Triangulation 3D | Ball Pivoting | Roll ball over point cloud |
| 3D Reconstruction | Poisson | Solve Poisson equation on normal field |
| Volume → Mesh | Marching Cubes | Per-voxel-cube isosurface extraction |
| Mesh Simplification | Quadric Error Metrics (QEM) | Collapse edges with min quadric error |
| Hole Filling | Ear clipping + Laplacian | Triangulate boundary → smooth fill |
| Outlier Removal | Statistical Outlier Removal | μ + α·σ distance threshold |
| Point Smoothing | Bilateral filter / MLS | Neighborhood-weighted reprojection |
| Noise Regularization | Voxel downsampling | Replace voxel contents with centroid |
| CT Reconstruction | Filtered Back-Projection | Radon transform + ramp filter + back-project |
| MRI | NMR + 2D FFT | T1/T2 relaxation; k-space Fourier |
| Medical Segmentation | U-Net (3D) | Encoder-decoder with skip connections |
| Tumor Detection | mpMRI + Dice loss training | T1c enhancement + T2 edema patterns |
| Bézier Curve | Bernstein polynomial | Weighted sum of control points |
| Bézier Surface | Tensor product Bernstein | Apply curve formula in both u, v |
| De Casteljau | Recursive linear interpolation | Stable evaluation + subdivision |

---

# Appendix B — Key Terms Glossary

**Alpha Shape:** Generalization of Delaunay triangulation parameterized by radius α; removes simplices whose circumradius exceeds 1/α.

**Augmented Reality (AR):** Overlaying virtual content on the real world in real time.

**Ball Pivoting Algorithm:** 3D triangulation by "rolling" a virtual ball over a point cloud.

**Bernstein Polynomial:** Basis functions for Bézier curves: Bᵢ,ₙ(t) = C(n,i)·tⁱ·(1−t)^(n−i).

**Bézier Curve:** Parametric curve defined by control points using Bernstein polynomial blending.

**Bézier Surface:** Tensor product of two Bézier curves; requires (m+1)×(n+1) control grid.

**BOLD fMRI:** Blood-Oxygen-Level-Dependent imaging; detects brain activity via oxygenated hemoglobin.

**BraTS Challenge:** Annual brain tumor segmentation competition (MICCAI); benchmark dataset.

**Convex Hull Property:** A Bézier curve lies entirely within the convex hull of its control points.

**De Casteljau's Algorithm:** Stable recursive algorithm for evaluating Bézier curves via repeated linear interpolation.

**Delaunay Triangulation:** Triangulation where no point lies inside any triangle's circumcircle; maximizes minimum angle.

**Dice Score (DSC):** Overlap metric: 2|A∩B|/(|A|+|B|); standard for segmentation evaluation.

**FLAIR:** Fluid-Attenuated Inversion Recovery MRI; suppresses CSF signal; highlights white matter lesions.

**Hounsfield Units (HU):** CT attenuation scale; water = 0, air = −1000, bone = +300 to +1900.

**ICP (Iterative Closest Point):** Aligns two point clouds by minimizing distances between correspondences.

**k-d Tree:** Binary spatial partition tree; O(log n) nearest-neighbor search.

**Larmor Frequency:** Proton precession frequency in MRI: f = γB₀/(2π); γ = 42.577 MHz/T.

**Level Set Method:** Represents evolving surfaces as zero-crossings of an implicit function φ; used in segmentation.

**LiDAR:** Light Detection And Ranging; measures distances by time-of-flight of laser pulses.

**Marching Cubes:** Extracts isosurface mesh from voxel grid; 256 cube configurations → triangles.

**MLS (Moving Least Squares):** Fits local polynomial to neighborhood; projects points onto smooth surface.

**NURBS:** Non-Uniform Rational B-Splines; generalization of Bézier curves with weights and knot vectors.

**Octree:** Recursive space subdivision into 8 octants; used for spatial indexing.

**Poisson Reconstruction:** Solves ∇²χ = ∇·V to reconstruct watertight surface from oriented points.

**QEM (Quadric Error Metrics):** Mesh simplification by iterative edge collapse minimizing sum-of-squared-distances-to-planes.

**SLAM:** Simultaneous Localization and Mapping; builds map and tracks pose concurrently.

**SOR (Statistical Outlier Removal):** Removes points with anomalously large average neighbor distances.

**T1/T2 Relaxation:** MRI relaxation times; T1 = longitudinal, T2 = transverse; contrast between tissue types.

**U-Net:** Encoder-decoder CNN with skip connections; dominant architecture for medical image segmentation.

**Virtual Reality (VR):** Fully synthetic immersive 3D environment, typically via HMD.

**Voronoi Diagram:** Dual of Delaunay triangulation; partitions space into cells nearest each point.

**Voxel:** Volumetric pixel; a cubic unit of a 3D grid (from "volumetric pixel").

**VIO (Visual-Inertial Odometry):** Combines camera and IMU for robust pose tracking; used in AR.

---

# Appendix C — Exam Strategy Guide

## What the Professor Explicitly Said to Focus On

1. **Three Key Formulas (computation exam questions):**
   - Bézier Curve formula (Bernstein form)
   - Bézier Surface formula (tensor product)
   - De Casteljau Algorithm (recursive evaluation)

2. **Theory questions will ask you to:**
   - **Describe** geometric modeling operations (triangulation, hole filling, noise removal, simplification)
   - **Give an example algorithm** for each operation
   - **Describe VR/AR** — how they work, tools, implementation

3. **Medical Imaging:**
   - Be able to compare MRI vs CT (input data, reconstruction method, clinical use)
   - Know what can be reconstructed from each modality
   - Reference the two Assignment 3 papers (brain tumor detection, signal detection in MRI)

## Recommended Approach to Theory Questions

**For any operation (e.g., triangulation):**
1. Define the problem (input → output)
2. Name at least one algorithm
3. Give the key idea of the algorithm in 2–3 sentences
4. Mention a practical application or limitation

**Example answer structure for "Explain triangulation from a 3D point cloud":**
> *A 3D point cloud is an unordered set of 3D coordinates with no topology. Triangulation converts it into a triangle mesh by inferring surface connectivity. The Ball Pivoting Algorithm (BPA) places a virtual sphere of radius ρ; as the sphere rolls over the points, each contact with a third point creates a triangle. Alternatively, Poisson Surface Reconstruction treats the problem globally: it estimates point normals, constructs a vector field, and solves a Poisson equation ∇²χ = ∇·V whose isosurface is the reconstructed mesh. Applications include 3D scanning, medical image visualization, and heritage preservation.*

## Memory Aids

**Bézier Degree 1-2-3 first term exponents:**
- Linear: (1−t)¹ ... t¹
- Quadratic: (1−t)² ... t²
- Cubic: (1−t)³ ... t³

**Binomial coefficients (Pascal's Triangle rows):**
```
n=1:  1 1
n=2:  1 2 1
n=3:  1 3 3 1
n=4:  1 4 6 4 1
n=5:  1 5 10 10 5 1
```

**De Casteljau mnemonics:**
- "Left-right lerp, then reduce": take two adjacent points, lerp by t, reduce count by 1, repeat
- Think of it as: you start with n+1 points and do n rounds, each round producing one fewer point

**MRI vs CT at a glance:**
```
MRI: No radiation · Strong magnet · Good for soft tissue · Slow · No ionizing
CT:  X-rays · Fast · Good for bone/lung · Hounsfield units · Ionizing radiation
```

---

*End of Study Book · Good luck on the exam!*
