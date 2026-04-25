# MRI and CT Scanning --- Complete Guide

> Wikipedia on MRI: "Magnetic resonance imaging (MRI) is a medical imaging technique used in radiology to generate pictures of the anatomy and the physiological processes inside the body. MRI scanners use strong magnetic fields, magnetic field gradients, and radio waves to form images of the organs in the body. MRI does not involve X-rays or the use of ionizing radiation, which distinguishes it from computed tomography (CT) and positron emission tomography (PET) scans."

---

## 1. CT Scanning (Computed Tomography)

### Physical Principle

X-ray CT uses ionizing radiation (X-rays). As X-rays pass through tissue they are absorbed:
```
I = I0 * exp(-Integral[mu(x)] dx)
```
where mu(x) is the linear attenuation coefficient. CT reconstructs the 3D map of mu(x,y,z).

### Hounsfield Units (HU)

Standardized scale of CT attenuation:
```
HU = 1000 * (mu_tissue - mu_water) / (mu_water - mu_air)
```

| Tissue | HU Range |
|---|---|
| Air | -1000 |
| Lung | -900 to -500 |
| Fat | -120 to -80 |
| Water / CSF | 0 |
| White matter | +20 to +30 |
| Grey matter | +35 to +45 |
| Blood | +50 to +80 |
| Liver | +40 to +65 |
| Calcification/bone | +100 to +1900 |

### CT Windowing

Display a range of HU values mapped to 0-255 gray:
- Window Level (WL) = center of the range
- Window Width (WW) = width of the range

| Window | WL | WW | Shows |
|---|---|---|---|
| Brain | 40 | 80 | Grey/white matter |
| Bone | 400 | 1800 | Bone detail |
| Lung | -600 | 1500 | Lung parenchyma |
| Abdomen | 60 | 400 | Soft tissue organs |
| Stroke | 40 | 40 | Acute hemorrhage |

### CT Reconstruction: Filtered Back-Projection (FBP)

CT acquisition = measuring the Radon transform (line integrals):
```
R_theta(s) = Integral[ mu(x,y) * delta(x*cos(theta) + y*sin(theta) - s) ] dx dy
```

FBP Algorithm:
```
1. For each angle theta:
   a. Acquire projection p_theta(s)
   b. Fourier transform: P_hat(f) = FT[p_theta(s)]
   c. Apply ramp filter: P_filtered(f) = |f| * P_hat(f)
   d. Inverse FT: p_filtered(s) = IFT[P_filtered(f)]

2. Back-project:
   mu(x,y) = Integral_0^pi  p_filtered(x*cos(theta) + y*sin(theta)) d(theta)
```

The ramp filter |f| compensates for the 1/f density of back-projected data.
In practice multiplied by Hamming/Hann window to reduce noise:
```
H(f) = |f| * (0.54 + 0.46*cos(pi*f/fmax))   [Hamming-windowed ramp]
```

### Iterative Reconstruction (IR) -- Modern CT

Model system as Ax = b:
- x = unknown attenuation image (vectorized)
- b = measured projections
- A = system matrix (each row = one ray integral)

Solve iteratively:
```
x_{k+1} = x_k - alpha * A^T * (A*x_k - b) + regularization
```

Benefits: 50-80% dose reduction for same image quality.
All modern scanners use IR: Siemens SAFIRE, GE ASIR, Philips iDose.

---

## 2. MRI Scanning

### Nuclear Magnetic Resonance Physics

Hydrogen nuclei (protons) in magnetic field B0 precess at Larmor frequency:
```
f0 = gamma * B0 / (2*pi)
gamma = 42.577 MHz/T for proton
```
At B0 = 1.5T: f0 = 63.87 MHz
At B0 = 3.0T: f0 = 127.74 MHz (radio frequency band)

### The Three Stages of MRI

1. ALIGNMENT: B0 creates net magnetization M0 along z-axis
   (1 in ~10^6 spins excess at body temperature)

2. EXCITATION: RF pulse at f0 tips magnetization:
   - 90 degree pulse: M tips fully into transverse (xy) plane
   - 180 degree pulse: M flips
   After excitation, precessing M induces voltage in receive coil -> MRI signal

3. RELAXATION:
   T1 recovery (longitudinal):  Mz(t) = M0 * (1 - exp(-t/T1))
   T2 decay (transverse):       Mxy(t) = Mxy0 * exp(-t/T2)
   T2* decay (with inhomogeneity): faster than T2

### T1 and T2 Times for Brain Tissues (at 3T)

| Tissue | T1 (ms) | T2 (ms) |
|---|---|---|
| White matter | 1110 | 69 |
| Grey matter | 1820 | 99 |
| CSF | 4000 | 2200 |
| Fat | 365 | 133 |
| Tumor (glioma) | 1500-2000 | 100-200 |
| Edema | 1900 | 150 |

### Spatial Encoding: k-Space

Gradient coils add spatially varying field to B0:
- Gz (slice selection): only slice where B0+Gz*z = f0/gamma excited
- Gy (phase encoding): phase of Mxy varies with y position
- Gx (frequency encoding): precession frequency varies with x during readout

Data acquired in k-space (spatial frequency domain):
```
kx = gamma/(2*pi) * Integral[Gx(t) dt]
ky = gamma/(2*pi) * Integral[Gy(t) dt]

Signal(kx,ky) = FT[proton_density(x,y)] (Fourier transform of image!)
```

Image reconstruction: 2D Inverse Fourier Transform of k-space data.

k-Space properties:
- Center: low frequencies -> overall brightness and contrast
- Edges: high frequencies -> fine detail and edges
- If only center acquired: blurry but fast (cardiac MRI uses this)

### MRI Sequences and Contrast

By varying TR (repetition time) and TE (echo time):

| Sequence | TR | TE | Bright | Dark | Clinical Use |
|---|---|---|---|---|---|
| T1-weighted | Short (<800ms) | Short (<30ms) | Fat, gadolinium, white matter | CSF | Anatomy, post-contrast |
| T2-weighted | Long (>2000ms) | Long (>80ms) | CSF, edema, most tumors | Fat | Pathology, lesions |
| FLAIR | Long | Long | White matter lesions | CSF suppressed | MS, glioma, stroke |
| DWI | --- | --- | Restricted diffusion | Free diffusion | Stroke, abscess |
| T1+Gd | Short | Short | Enhancing regions | --- | Tumor vascularity, BBB breakdown |
| SWI | Long | Long | --- | Hemosiderin, deoxy-Hb | Bleeds, veins, iron |

### Advanced MRI Techniques

**Diffusion Tensor Imaging (DTI):**
Measures diffusion anisotropy -> maps white matter tracts (tractography).
Pre-surgical planning: avoid eloquent white matter fibers.
ADC (Apparent Diffusion Coefficient): low in stroke, high-grade tumor.

**Perfusion MRI (DSC):**
Dynamic tracking of Gadolinium bolus -> cerebral blood volume (CBV).
High rCBV = high vascularity = high-grade tumor.

**MR Spectroscopy (MRS):**
Chemical peaks in spectrum:
- NAA (N-acetyl aspartate) at 2.0 ppm: neurons (REDUCED in tumor)
- Cho (choline) at 3.2 ppm: cell membranes (ELEVATED in tumor)
- Cr (creatine) at 3.0 ppm: energy metabolism (reference)
- Lac (lactate) at 1.3 ppm: anaerobic metabolism (necrosis/high-grade)
- Lip (lipids): necrotic tumor

**Elevated Cho/NAA ratio > 2.0** strongly suggests high-grade glioma.

---

## 3. CT vs MRI Comparison

| Aspect | CT | MRI |
|---|---|---|
| Physical principle | X-ray attenuation | NMR of protons |
| Radiation | Ionizing (X-rays) | Non-ionizing (RF + magnets) |
| Acquisition time | 5-60 seconds | 20-60 minutes |
| Resolution | 0.5-1mm isotropic | 1-3mm typical |
| Bone/calcification | Excellent | Poor (no signal) |
| Soft tissue | Moderate | Excellent |
| Hemorrhage (acute) | Bright (hyperdense) | Depends on sequence |
| Brain tumors | Shows mass, edema | Shows tumor sub-regions |
| Stroke | Early: often normal; late: hypodense | DWI: bright within minutes |
| Cost | Lower | Higher |
| Main limitation | Radiation dose | Slow, contraindications (metal) |
| Claustrophobia | Rare | Common |

---

## 4. 3D Reconstruction Pipeline

```
DICOM files (512x512 x N slices)
    |
    v
Read with pydicom/SimpleITK -> numpy array
    |
    v
Preprocessing:
  - Normalize HU values
  - Resample to isotropic voxel spacing (e.g., 1mm x 1mm x 1mm)
  - Apply Gaussian smoothing (sigma=0.5-1.0)
    |
    v
Segmentation:
  - Thresholding (Otsu) or
  - Region growing or
  - Deep learning (U-Net, nnU-Net)
    |
    v
Marching Cubes (isovalue = 0.5)
  -> Triangle mesh
    |
    v
Post-processing:
  - Laplacian smoothing
  - QEM simplification (target: 100k-500k triangles)
    |
    v
Visualization (VTK, 3D Slicer) or 3D printing (STL)
```

---

*Sources: Wikipedia Magnetic resonance imaging; Wikipedia Computed tomography; 
Bushberg et al. 'The Essential Physics of Medical Imaging'; 
Netter 'Atlas of Human Anatomy'*
