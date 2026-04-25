# Virtual Reality & Augmented Reality --- Complete Guide

> Wikipedia on VR: "Virtual reality (VR) is a simulated experience that employs 3D head-mounted displays and pose tracking to give the user an immersive feel of a virtual world."
> Wikipedia on AR: "Augmented reality (AR) overlays real-time 3D-rendered computer graphics into the real world through a display. Augmented reality can be defined as a system that incorporates three basic features: a combination of real and virtual worlds, real-time interaction, and accurate 3D registration of virtual and real objects."

---

## 1. The Reality-Virtuality Continuum (Milgram 1994)

```
Real World <---------------------------------------> Virtual World
           |              |              |
           AR             MR            AV
      (Augmented    (Mixed Reality)  (Augmented      (VR)
        Reality)                     Virtuality)
```

- AR: Mostly real + virtual overlay
- MR: Real and virtual interact
- AV: Mostly virtual, some real inserted
- VR: 100% synthetic environment

---

## 2. VR Core Requirements

### 6 Degrees of Freedom (6-DoF)

Translation:  X (left/right), Y (up/down), Z (forward/back)
Rotation:     Pitch (nod), Yaw (shake head), Roll (tilt)

All 6 must be tracked in real time to avoid motion sickness.

### Performance Requirements

| Metric | Minimum | Target | Premium |
|---|---|---|---|
| Frame rate | 60 fps | 90 fps | 120 fps |
| Latency (motion-to-photon) | 20 ms | 10 ms | 7 ms |
| Resolution (per eye) | 1600x1440 | 2064x2208 | 4K+ |
| Field of View | 90 deg | 110 deg | 120+ deg |

### Why < 20ms Latency Matters

The vestibular system detects head movement within 2-5ms. The visual system must confirm
the movement within ~20ms or the mismatch causes simulator sickness (nausea, disorientation).

---

## 3. VR Tracking Technologies

### Inside-Out Tracking (Modern Standard)
- Cameras on the HMD observe the environment
- SLAM/VIO algorithms compute device pose from observed features
- No external infrastructure needed
- Devices: Meta Quest 2/3/Pro, HoloLens 2, Apple Vision Pro
- Accuracy: 1-3mm position, <0.1 degree rotation

### Outside-In Tracking (High-End PC VR)
- External base stations emit IR laser sweeps (Lighthouse tracking)
- Sensors on HMD and controllers triangulate position
- Devices: Valve Index, HTC Vive, HTC Vive Pro
- Accuracy: <1mm position (more precise than inside-out)

### IMU (Inertial Measurement Unit)
- All HMDs include IMU: accelerometer + gyroscope
- Provides high-frequency (1000 Hz) rotation data
- Fused with camera data via Extended Kalman Filter (EKF)
- Alone: fast but drifts over time; with vision: stable

### Visual-Inertial Odometry (VIO)
The gold standard. Camera provides absolute position via feature matching.
IMU provides 1000 Hz rotation between video frames (30-60 fps).
EKF/Kalman filter fuses them: accurate, drift-corrected, low-latency.

ORB-SLAM3 (arXiv:2007.11898) is the state-of-the-art open-source VIO system:
- Features: ORB (Oriented FAST + Rotated BRIEF) - fast and rotation invariant
- MAP estimation: optimizes all poses + map points jointly
- Multi-map: when tracking lost, starts new sub-map; later merges
- Accuracy: 3.6cm on EuRoC drone dataset, 9mm hand-held

---

## 4. VR Display Technologies

### OLED vs LCD
| Property | OLED | LCD |
|---|---|---|
| Black level | True black (pixel off) | Backlit (gray black) |
| Contrast | Very high (1,000,000:1) | Lower (1,000:1) |
| Response time | <0.1ms | 1-5ms (ghosting risk) |
| Burn-in | Yes (static images) | No |
| Brightness | Lower | Higher |
| Used in | PSVR2, Valve Index | Meta Quest 2 |

### Optics Types
- Fresnel: Concentric rings; wide FoV; light; some god-rays
- Pancake: Multiple reflective surfaces; thin/compact; dimmer
  (Meta Quest 3, Apple Vision Pro use pancake)
- Catadioptric: Hybrid reflective; used in Varjo headsets

### Vergence-Accommodation Conflict (VAC)
Eyes converge (rotate) to virtual object depth but must accommodate (focus lens)
to fixed screen distance (~2m optical). Causes eye strain in prolonged use.
Solutions:
- Varifocal displays: Mechanically move lens based on eye tracking
- Light field displays: Multiple focal planes (computational lightfield)
- Holographic displays: Wave optics, true 3D light field (future)

---

## 5. Rendering Techniques for VR

### Foveated Rendering
- Fovea (center of retina): 2 degrees, maximum acuity
- Periphery: 80% of visual field but 50% lower acuity
- With eye tracking: render only foveal region at full quality
- Periphery: 25-50% lower resolution (user cannot detect)
- GPU savings: 3-5x reduction in shading cost

Devices with eye tracking: Apple Vision Pro, PlayStation VR2, Varjo headsets

### Asynchronous Spacewarp (ASW) / Timewarp
If GPU drops below 90 fps: instead of judder (dropped frame), the runtime
extrapolates the next frame by warping the last rendered frame using depth + motion.
User perceives smooth 90fps even if game renders at 45fps.

### Single-Pass Stereo Rendering
Render both eyes in one draw call using:
- Geometry shaders (instancing to two render targets)
- Multi-view extension (GL_OVR_multiview, VK_KHR_multiview)
- Reduces CPU-GPU draw call overhead by ~40%

### Lens Distortion Pre-correction
Fresnel lenses create barrel distortion (edges bow outward).
Renderer applies inverse pincushion distortion to the image.
The lens then corrects it back to a straight image.
Separate distortion maps for R, G, B channels to correct chromatic aberration.

---

## 6. AR: How It Works

### Three Core Problems
1. TRACKING: Know device pose (6-DoF) in real world at all times
2. REGISTRATION: Align virtual content precisely to real world coordinates (pixel-perfect)
3. RENDERING: Blend virtual content with real world (occlusion, lighting, shadows)

### Marker-Based AR Pipeline
```
Camera frame
    |
    v
Grayscale + adaptive threshold -> binary image
    |
    v
Contour detection -> find quadrilateral candidates
    |
    v
Decode marker ID (bit pattern in interior grid)
    |
    v
PnP (Perspective-n-Point) pose estimation:
  Known 3D corners [(-s,-s,0),(s,-s,0),(s,s,0),(-s,s,0)]
  Observed 2D projections
  Solve: minimize Sum |projected(R,t,P3d_i) - p2d_i|^2
  -> Camera pose (R,t) given camera intrinsics K
    |
    v
Render virtual object at pose (R,t)
```

### Markerless (SLAM-based) AR Pipeline
```
Camera frame
    |
    v
Feature extraction (ORB/SIFT/SuperPoint): keypoints + descriptors
    |
    v
Feature matching to active map (Bag-of-Words + descriptor match)
    |
    v
Pose estimation (P3P + RANSAC inlier filtering)
    |
    v
Local optimization: Bundle Adjustment on recent keyframes
    |
    v
Map expansion: triangulate new 3D points from matched features
    |
    v
Loop closure: DBoW2 similarity query -> global optimization if loop found
```

### Plane Detection (ARKit/ARCore)
LiDAR (iPhone 12 Pro+) or stereo gives depth map.
RANSAC plane fitting: for each candidate plane, count inlier depth points.
Plane tracked over time; boundary refined using alpha shapes.
Used for: placing virtual furniture on floors, wall projections.

---

## 7. Key Hardware 2024

| Device | Type | Tracking | Display | Notable |
|---|---|---|---|---|
| Meta Quest 3 | Standalone VR/AR | Inside-out | LCD pancake | Color passthrough, affordable |
| Apple Vision Pro | AR/VR spatial | Inside-out | MicroOLED | Eye/hand tracking, visionOS |
| PlayStation VR2 | Tethered VR | Inside-out | OLED | Adaptive triggers, eye tracking |
| Valve Index | Tethered VR | Lighthouse | LCD | Finger tracking, widest FoV |
| HoloLens 2 | AR enterprise | Inside-out | Waveguide | Enterprise AR, hand tracking |
| Magic Leap 2 | AR enterprise | Inside-out | Waveguide | Dimming dimmer, focus modes |

---

## 8. Applications

### Medical
- Surgical planning: overlay CT/MRI anatomy in AR on patient
- Training: VR surgical simulation (Osso VR, Touch Surgery)
- Rehabilitation: VR stroke/motor retraining
- Pain management: VR distraction reduces pain 35-50%

### Industrial
- Boeing: AR wiring guidance -> 40% error reduction, 25% faster
- Remote assistance: Expert annotates worker's live view
- Digital twin: 1:1 scale VR walkthrough before manufacturing

### Education
- Virtual anatomy (Complete Anatomy, Visible Body)
- Historical reconstruction (ancient Rome, Pompeii VR)
- VR physics labs (dangerous experiments safely)

---

## 9. Novel Rendering for VR/AR: NeRF and Gaussian Splatting

### NeRF (arXiv:2003.08934)
Neural Radiance Fields -- photorealistic novel view synthesis:
- Scene = MLP neural network F(x,y,z,theta,phi) -> RGB + density
- Rendering: integrate color along rays via volume rendering
- Input: 20-100 photos with known poses
- Training: 1-2 days; rendering: 30s/frame (slow)
- View-dependent effects: reflections, specular highlights captured

### 3D Gaussian Splatting (arXiv:2308.04079)
Real-time alternative to NeRF:
- Scene = millions of 3D Gaussians (position, covariance, color, opacity)
- Rendering: project Gaussians to 2D, alpha-composite front-to-back
- Training: 30 minutes; rendering: 30+ fps at 1080p
- Application: Scan real space with phone -> photorealistic VR/AR environment

---

*Sources: Wikipedia Virtual reality; Wikipedia Augmented reality; ORB-SLAM3 (arXiv:2007.11898); NeRF (arXiv:2003.08934); 3DGS (arXiv:2308.04079)*
