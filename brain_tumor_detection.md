# Brain Tumor Detection --- Complete Guide

## 1. Overview of Brain Tumors

### Classification
- Primary: Originate in brain tissue
  - Gliomas (most common): astrocytoma, glioblastoma (GBM), oligodendroglioma
  - Meningioma: from meninges, usually benign
  - Pituitary adenoma
  - Medulloblastoma (pediatric)
- Secondary (metastatic): Spread from elsewhere (lung, breast, melanoma)

### WHO Grading (2021 Classification)
- Grade 1: Slow-growing, often resectable (e.g., pilocytic astrocytoma)
- Grade 2: Diffuse, infiltrating; low mitotic activity
- Grade 3: Malignant features, mitoses (anaplastic glioma)
- Grade 4: High mitotic activity, necrosis, microvascular proliferation (GBM)

**GBM (Glioblastoma Multiforme):**
- Most common primary brain malignancy in adults
- Median survival: 14-16 months with maximal treatment
- Hallmarks: ring enhancement (T1c), central necrosis, peritumoral edema (T2/FLAIR)

---

## 2. BraTS Dataset and Challenge

### International Brain Tumor Segmentation Challenge (arXiv:1811.02629)
Annual challenge at MICCAI (premier medical image computing conference).
Running since 2012. BraTS 2023: 1251 training cases.

### Four MRI Modalities per Patient
```
T1:    Anatomy, structural details
T1ce:  Post-contrast; shows blood-brain barrier breakdown (active tumor: BRIGHT)
T2:    Edema and infiltration (tumor + edema: BRIGHT)
FLAIR: Edema without CSF (tumor/edema: BRIGHT, CSF: DARK)
```

### Tumor Sub-region Labels

BraTS uses 3 nested labels:

```
Whole Tumor (WT)  = everything: enhancing + necrosis + edema
Tumor Core (TC)   = enhancing + necrosis (without edema)
Enhancing Tumor (ET) = only the gadolinium-enhancing active tumor
```

In voxel labels:
- Label 1: Necrotic core (non-enhancing tumor core)
- Label 2: Peritumoral edematous/invaded tissue
- Label 4: GD-enhancing tumor

### Evaluation Metrics
```
Dice Score = 2*|prediction AND ground_truth| / (|prediction| + |ground_truth|)
```
Range [0,1]. 1 = perfect. Typical state-of-the-art: ~0.90 WT, ~0.86 TC, ~0.83 ET.

Hausdorff Distance 95th percentile (HD95): Surface distance in mm.
State-of-the-art: ~3-5mm.

---

## 3. Clinical MRI Features for Brain Tumors

### Glioblastoma (GBM) - Grade 4
| Sequence | Appearance |
|---|---|
| T1 | Hypointense mass; may show isointense core |
| T1ce | RING ENHANCEMENT (hallmark!) around necrotic core |
| T2 | Hyperintense tumor + extensive surrounding edema |
| FLAIR | Hyperintense mass + edema; suppresses CSF |
| DWI | Rim of restricted diffusion (high cellularity at enhancing border) |
| ADC | Low ADC at enhancing rim; elevated in necrosis and edema |
| Perfusion (rCBV) | ELEVATED (high vascularity = high grade) |
| Spectroscopy | High Cho, low NAA, Lac+Lip peaks (necrosis) |

### Lower Grade Glioma (Grade 2-3)
- T2/FLAIR: Hyperintense, diffusely infiltrating, no clear boundary
- T1ce: Little or no enhancement (no BBB disruption)
- DWI: Not usually restricted
- Spectroscopy: Mildly elevated Cho

### Metastases
- T1ce: SOLID RING or homogeneous enhancement
- T2: Variable; usually distinct spherical mass
- Multiple lesions: strongly suggests metastases over primary
- Located at grey-white matter junction (blood-borne distribution)

---

## 4. Deep Learning for Brain Tumor Segmentation

### U-Net for Brain Tumor Segmentation (2015-)

U-Net (arXiv:1505.04597) applied to brain tumor:
- Input: 4-channel volume (T1, T1ce, T2, FLAIR) concatenated
- 3D U-Net: processes volumetric data directly
- Output: Per-voxel class probability for 4 classes (background + 3 tumor labels)

Key adaptations for brain tumor:
- Residual connections within encoder/decoder blocks
- Deep supervision: loss at multiple decoder levels
- Patch-based training: random 128x128x128 patches
- Test-time augmentation: flip along all axes, average predictions

### nnU-Net (2021) - State of the Art

Self-configuring U-Net that automatically determines:
- Patch size (based on GPU memory and dataset statistics)
- Batch size
- Normalization strategy (z-score, percentile clipping)
- Architecture type (2D, 3D, 3D cascade)
- Data augmentation (elastic deformation, random rotation, scaling, flipping)

nnU-Net outperforms hand-tuned architectures on 23/23 medical segmentation benchmarks.
For BraTS 2021: DSC 0.892 WT, 0.865 TC, 0.832 ET.

### Transformer-Based Methods

TransBTS (MICCAI 2021):
```
3D CNN encoder -> flatten spatial features to sequence
                -> Transformer encoder (multi-head self-attention)
                -> CNN decoder with skip connections
```
Self-attention captures long-range dependencies (critical for irregular tumor shapes).

SwinUNETR (CVPR 2022):
- Hierarchical Swin Transformer backbone (arXiv:2103.14030)
- Shifted Window self-attention: linear complexity w.r.t. volume size
- Pretraining on large unlabeled medical datasets
- State-of-the-art on BraTS 2021

---

## 5. Automated Brain Tumor Analysis Pipeline

```
Multi-parametric MRI acquisition (T1, T1ce, T2, FLAIR)
    |
    v
Preprocessing:
  1. Co-registration: align all 4 modalities to T1 atlas (FSL FLIRT, ANTs)
  2. Brain extraction (skull stripping): BET, HD-BET
  3. Intensity normalization: z-score or percentile normalization
    |
    v
Segmentation (nnU-Net or SwinUNETR):
  Input: (4, 240, 240, 155) tensor
  Output: (4-class, 240, 240, 155) probability maps
    |
    v
Post-processing:
  Argmax -> segmentation mask
  Remove small connected components (< 100 voxels)
  Apply brain mask
    |
    v
Radiomic Feature Extraction:
  - Shape: volume, surface area, elongation, sphericity
  - Intensity statistics: mean, variance, skewness, kurtosis
  - Texture (GLCM, GLRLM, GLSZM)
  - Wavelet sub-band features
    |
    v
Clinical Prediction:
  - Overall survival prediction (regression/classification)
  - IDH mutation prediction (AUC ~0.85)
  - Pseudoprogression vs true progression
```

---

## 6. Key Papers

| Paper | Year | Innovation | Performance |
|---|---|---|---|
| U-Net (Ronneberger) | 2015 | Skip connections, data augmentation | BraTS DSC ~0.78 |
| 3D U-Net (Cicek) | 2016 | 3D skip connections | DSC ~0.82 |
| Kamnitsas et al. | 2017 | 3D DeepMedic (dual-path CNN) | DSC ~0.85 |
| nnU-Net (Isensee) | 2018 | Self-configuring | DSC ~0.87 |
| TransBTS | 2021 | CNN+Transformer hybrid | DSC ~0.89 |
| SwinUNETR | 2022 | Swin Transformer backbone | DSC ~0.91 |
| BraTS 2023 winners | 2023 | Ensemble + TTA | DSC ~0.92 |

---

## 7. Tools and Libraries

| Tool | Purpose |
|---|---|
| 3D Slicer | DICOM viewer, segmentation, volume rendering |
| ITK/SimpleITK | Medical image I/O and processing (Python/C++) |
| MONAI | PyTorch-based medical AI framework |
| nnU-Net | Self-configuring medical segmentation |
| pydicom | Read/write DICOM in Python |
| ANTs | Image registration and brain extraction |
| FSL | Brain extraction tool (BET), FAST tissue segmentation |
| FreeSurfer | Cortical parcellation, brain surface extraction |
| HD-BET | Deep learning brain extraction |

---

*Sources: BraTS Challenge (arXiv:1811.02629); Bakas et al. multi-year challenge papers; 
Isensee et al. nnU-Net; Wikipedia Brain tumor; clinical radiology references*
