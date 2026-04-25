# Advanced Exam Booster Pack (Internet-Researched)

## How to Use This Packet in a 2-Hour Written Exam
- First 5 minutes: write the core formulas from memory on scratch paper (Bernstein basis, De Casteljau recurrence, Dice score, HU equation, Radon/FBP, Delaunay in-circle determinant).
- Next 5 minutes: skim question verbs (define, derive, compare, compute) and allocate minutes per mark.
- For compute questions: show intermediate arithmetic (even if final answer is wrong you recover method marks).
- For theory questions: always include (1) definition, (2) key equation, (3) practical implication/example, (4) limitation.

---

## 1) VR/AR: Advanced Talking Points That Score Well

### 1.1 End-to-End XR Pipeline (What examiners want)
1. Sensor acquisition (IMU/camera/depth)
2. Time synchronization and calibration
3. Visual-inertial odometry (state estimation)
4. Pose prediction to display time
5. Stereo rendering
6. Lens distortion correction and timewarp
7. Scan-out on display

**Why this matters:** motion-to-photon latency is cumulative across all stages. Reducing only GPU time is not enough if tracking/prediction is weak.

### 1.2 Tracking Fusion (state-estimation form)
State vector example:
- position p, velocity v, orientation q, IMU biases b_g, b_a

Discrete process model (concept):
- x_k = f(x_{k-1}, u_k) + w_k
- z_k = h(x_k) + n_k

Where IMU drives prediction, camera features correct drift (EKF / bundle-adjustment style back-end).

### 1.3 OpenXR High-Value Notes
- OpenXR 1.1 was announced by Khronos on **April 15, 2024**.
- 1.1 promotes widely-used extension capabilities into core to reduce runtime fragmentation.
- Exam framing: “OpenXR decouples application code from vendor SDKs by standardizing instance/session/swapchain/action abstractions.”

### 1.4 AR Registration Error Sources
- Intrinsic calibration error (focal length, principal point)
- Extrinsic drift from SLAM
- Rolling shutter + fast motion
- Lighting changes causing feature tracking loss

**Strong answer line:** “AR realism depends on geometric, photometric, and temporal consistency—not just geometric alignment.”

---

## 2) Delaunay Triangulation: Beyond the Basics

### 2.1 In-Circle Test (orientation-aware)
For CCW triangle (A,B,C), point D is inside circumcircle if determinant > 0:

|Ax-Dx  Ay-Dy  (Ax-Dx)^2+(Ay-Dy)^2|
|Bx-Dx  By-Dy  (Bx-Dx)^2+(By-Dy)^2|  > 0
|Cx-Dx  Cy-Dy  (Cx-Dx)^2+(Cy-Dy)^2|

If orientation is CW, sign flips.

### 2.2 Why Delaunay in graphics/geometry pipelines
- Better-conditioned finite elements (larger minimum angles)
- Cleaner interpolation over irregular samples
- Stable neighborhood graph for point clouds
- Dual Voronoi structure enables nearest-region reasoning

### 2.3 Robustness pitfalls (great exam bonus)
- Nearly cocircular points -> floating point ambiguity
- Collinear subsets -> degenerate triangles
- Duplicate points -> broken predicates

Mitigations:
- symbolic perturbation / exact predicates (Shewchuk-style orientation/in-circle)
- epsilon-aware duplicate filtering
- deterministic tie-breaks

### 2.4 Complexity statements to memorize
- Bowyer-Watson expected: O(n log n)
- Worst-case for many practical incremental methods: O(n^2)
- Planar triangulation edge count (general position): about 3n - 3 - h

---

## 3) Marching Cubes: Topology-Correct Thinking

### 3.1 Core idea (exam-safe wording)
Given a scalar field sampled at grid corners, classify each cube corner against an isovalue, then emit triangles from a lookup table and interpolate vertex positions on intersected edges.

### 3.2 Interpolation formula
t = (iso - f1) / (f2 - f1)

p = p1 + t (p2 - p1)

### 3.3 Ambiguity handling hierarchy
1. Original MC (15 symmetry classes)
2. Asymptotic Decider (face ambiguity resolution)
3. MC33 (topology-aware case expansion)

### 3.4 Normal computation for shading
- Analytical: normal = gradient of trilinear field
- Practical finite difference:
  - fx ~ f(x+1)-f(x-1)
  - fy ~ f(y+1)-f(y-1)
  - fz ~ f(z+1)-f(z-1)
- Normalize and interpolate to vertices

### 3.5 Practical mesh quality improvements
- Deduplicate edge vertices with hash map keyed by (cell,edge)
- Apply Taubin/Laplacian smoothing cautiously (avoid volume shrink)
- Use manifold checks before downstream FEM/printing

---

## 4) CT + MRI: High-Yield Physics and Reconstruction

### 4.1 CT attenuation model
I = I0 exp(-∫ mu(s) ds)

Log form used in reconstruction:
- ln(I/I0) = -∫ mu(s) ds

### 4.2 Hounsfield Unit equation
HU = 1000 * (mu_tissue - mu_water) / (mu_water - mu_air)

Anchor values:
- air ≈ -1000
- water = 0
- dense cortical bone up to +1000 or higher

### 4.3 Filtered Backprojection intuition
- Raw backprojection blurs as 1/r
- Ramp filter compensates high-frequency loss
- Then integrate filtered projections over angles

### 4.4 MRI signal essentials
- Larmor relation: omega0 = gamma B0
- Contrast depends on TR, TE, tissue T1/T2/T2*

Classic contrast shortcuts:
- T1-weighted: fat bright, fluid dark
- T2-weighted: fluid bright
- FLAIR: fluid suppressed; edema/tumor remains bright

### 4.5 MRI safety talking points
- MRI has no ionizing radiation (contrast with CT)
- Main hazards: projectile risk, RF heating/burns, acoustic noise, implant/device interactions

---

## 5) Brain Tumor Segmentation (BraTS-Oriented)

### 5.1 Label semantics (critical)
- WT (whole tumor): edema + core + enhancing
- TC (tumor core): necrosis/non-enhancing + enhancing (no edema)
- ET (enhancing tumor): active contrast-enhancing component

### 5.2 Metrics you should be ready to compute
Dice(A,B) = 2|A∩B| / (|A|+|B|)

Precision = TP/(TP+FP)
Recall = TP/(TP+FN)

HD95: 95th percentile bidirectional boundary distance

### 5.3 Training details examiners love
- 3D patch sampling to fit memory
- class-balanced sampling (tumor voxels are minority)
- z-score normalization per modality
- deep supervision for stable gradients
- test-time ensembling/augmentation for better robustness

### 5.4 Error analysis language
- False positives near ventricles or postoperative cavities
- Boundary leakage into edema for ET/TC confusion
- Domain shift across scanners/sites/protocols

---

## 6) Bézier Curves: Advanced Differentiation + Continuity

### 6.1 General form
B(t) = Σ_{i=0..n} C(n,i) (1-t)^(n-i) t^i P_i

### 6.2 First derivative curve (degree n-1)
B'(t) = n Σ_{i=0..n-1} B_{i,n-1}(t) (P_{i+1}-P_i)

Endpoint tangents:
- B'(0) = n(P1-P0)
- B'(1) = n(Pn-P_{n-1})

### 6.3 Second derivative (useful for curvature discussion)
B''(t) = n(n-1) Σ_{i=0..n-2} B_{i,n-2}(t)(P_{i+2}-2P_{i+1}+P_i)

### 6.4 Joining segments (exam favorite)
Given curve A ending at A3 and curve B starting at B0:
- C0 continuity: A3 = B0
- C1 continuity: A3-A2 = B1-B0
- G1 continuity: directions parallel (magnitudes may differ)
- C2 continuity: second derivatives equal at join

### 6.5 Subdivision at t=0.5 (De Casteljau)
- Produces two Bézier segments exactly matching original
- Useful for adaptive tessellation and collision approximation

---

## 7) Bézier Surfaces: Differential Geometry Essentials

For tensor-product surface S(u,v):
S(u,v)=Σ_i Σ_j B_{i,m}(u) B_{j,n}(v) P_{i,j}

### 7.1 Partial derivatives
Su = ∂S/∂u
Sv = ∂S/∂v

Surface normal (unnormalized):
N = Su × Sv

### 7.2 Boundary curves
- Fix u=0,1 or v=0,1 to get Bézier boundary curves
- Corner interpolation always holds: S(0,0)=P00, etc.

### 7.3 Continuity between adjacent patches
- C0: shared boundary control points match
- C1 across shared edge: adjacent handle rows/columns arranged collinearly with matched derivative magnitudes

---

## 8) High-Probability Computation Drills

### Drill A: Dice score
If |GT|=1200, |Pred|=1000, intersection=900:
Dice = 2*900 / (1200+1000) = 1800/2200 = 0.8182

### Drill B: De Casteljau quadratic
P0=(0,0), P1=(2,2), P2=(4,0), t=0.25
Q0=0.75P0+0.25P1=(0.5,0.5)
Q1=0.75P1+0.25P2=(2.5,1.5)
B=0.75Q0+0.25Q1=(1.0,0.75)

### Drill C: Marching edge interpolation
f1=30, f2=90, iso=60, p1=(0,0,0), p2=(0,1,0)
t=(60-30)/(90-30)=0.5
p=(0,0.5,0)

### Drill D: CT window mapping
Given WL=40, WW=80:
visible HU range is [0,80]
HU below 0 -> black, above 80 -> white (after clipping)

---

## 9) One-Page Formula Dump (Memorize)
- Bernstein: B_{i,n}(t)=C(n,i)t^i(1-t)^(n-i)
- Bézier curve: B(t)=Σ B_{i,n}(t)P_i
- De Casteljau: P_i^{(j)}=(1-t)P_i^{(j-1)}+tP_{i+1}^{(j-1)}
- Bézier derivative: B'(t)=nΣ B_{i,n-1}(t)(P_{i+1}-P_i)
- Surface: S(u,v)=ΣΣ B_{i,m}(u)B_{j,n}(v)P_{i,j}
- Dice: 2TP/(2TP+FP+FN)
- HU: 1000(mu_t-mu_w)/(mu_w-mu_a)
- CT attenuation: I=I0 exp(-∫mu ds)
- Larmor: omega0=gamma B0
- Marching interpolation: p=p1 + ((iso-f1)/(f2-f1))(p2-p1)

---

## 10) Curated Research References (for trustable facts)
1. OpenXR Registry (official specification): https://registry.khronos.org/OpenXR/specs/1.1-khr/html/xrspec.html
2. Khronos press release (OpenXR 1.1, 2024-04-15): https://www.khronos.org/news/press/khronos-releases-openxr-1.1-to-further-streamline-cross-platform-xr-development
3. ORB-SLAM3 (arXiv:2007.11898): https://arxiv.org/abs/2007.11898
4. U-Net (arXiv:1505.04597): https://arxiv.org/abs/1505.04597
5. nnU-Net (Nature Methods 2021): https://www.nature.com/articles/s41592-020-01008-z
6. BraTS benchmark review (arXiv:1811.02629): https://arxiv.org/abs/1811.02629
7. BraTS 2024 post-treatment glioma challenge: https://arxiv.org/abs/2405.18368
8. BraTS 2024 MEN-RT challenge: https://arxiv.org/abs/2405.18383
9. Marching Cubes (SIGGRAPH 1987): https://doi.org/10.1145/37401.37422
10. FDA MRI professional safety page: https://www.fda.gov/radiation-emitting-products/mri-magnetic-resonance-imaging/information-professionals
11. NIBIB MRI overview: https://www.nibib.nih.gov/science-education/science-topics/magnetic-resonance-imaging-mri
12. WHO CNS Tumours (5th edition volume, 2021): https://publications.iarc.who.int/601
