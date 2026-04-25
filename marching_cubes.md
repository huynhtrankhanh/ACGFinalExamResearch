# Marching Cubes --- Complete Guide

> Wikipedia says: "Marching cubes is a computer graphics algorithm, published in the 1987 SIGGRAPH proceedings by Lorensen and Cline, for extracting a polygonal mesh of an isosurface from a three-dimensional discrete scalar field."
> "The applications are mainly concerned with medical visualizations such as CT and MRI scan data images."

---

## 1. Problem Statement

**Input:** 3D scalar field f(x,y,z) sampled on a regular grid (voxels)
         e.g., CT scan (Hounsfield units), MRI intensity, distance field

**Output:** Triangle mesh of the isosurface {(x,y,z) : f(x,y,z) = isovalue}

**Example:** Extract a brain surface from MRI by thresholding at the grey matter / CSF boundary.

---

## 2. Algorithm Steps

```
For each 2x2x2 voxel cube in the grid:
  1. CLASSIFY: Label each of 8 corners as inside (f > isovalue) or outside (f <= isovalue)
  
  2. INDEX: Convert 8 binary labels to an 8-bit integer (index 0..255)
     bit 0 = corner 0, bit 1 = corner 1, ..., bit 7 = corner 7
  
  3. LOOKUP: Use triTable[index] to get the list of triangle edges (up to 5 triangles)
  
  4. INTERPOLATE: For each triangle edge crossing the isosurface, linearly interpolate:
     t = (isovalue - f(v1)) / (f(v2) - f(v1))
     vertex = v1 + t * (v2 - v1)
  
  5. OUTPUT: Store triangle vertices
```

---

## 3. The 256 Cases -> 15 Unique Cases

By exploiting rotational and reflective symmetry, all 256 possible corner configurations
reduce to 15 unique cases:

```
Case 0:  All outside -> no triangles
Case 1:  1 corner inside -> 1 triangle (corner cut)
Case 2:  2 adjacent corners inside -> 1 triangle
Case 3:  2 diagonal corners inside -> 2 triangles (ambiguous!)
Case 4:  1 corner inside (opposite side) -> 1 triangle
Case 5:  3 corners of a face inside -> 2 triangles
...
Case 14: 7 corners inside (1 outside) -> 1 triangle (complement of case 1)
Case 15: All inside -> no triangles
```

The original paper had 15 cases (reduced by symmetry).
Marching Cubes 33 (Chernyaev 1995) expands to 33 cases to resolve topological ambiguities.

---

## 4. Linear Interpolation Along Edges

When an edge crosses the isosurface:

```
t = (isovalue - f_v1) / (f_v2 - f_v1)

vertex = v1 + t * (v2 - v1)
       = (1-t)*v1 + t*v2
```

This places the vertex at the exact isovalue crossing within the edge.

**Example:** edge from (0,0,0) with f=10 to (1,0,0) with f=30, isovalue=20:
```
t = (20 - 10) / (30 - 10) = 10/20 = 0.5
vertex = (0,0,0) + 0.5 * (1,0,0) = (0.5, 0, 0)
```

---

## 5. Normal Estimation

The gradient of the scalar field gives the surface normal at each vertex:
```
N(x,y,z) = grad(f) = (df/dx, df/dy, df/dz)

Finite differences:
df/dx ~ (f(x+1,y,z) - f(x-1,y,z)) / 2
```

Interpolate normals from grid vertices to triangle vertices the same way as positions.

---

## 6. Ambiguous Cases and Marching Cubes 33

**Face ambiguity:** When opposite corners of a cube face are both inside/outside,
the surface crossing pattern is ambiguous (two valid triangulations).

**Interior ambiguity:** Even with face ambiguities resolved, some cube configurations
have multiple valid interior triangulations.

**Asymptotic Decider (Nielson & Hamann 1991):** Test based on the trilinear interpolant's
saddle point to resolve face ambiguities.

**Marching Cubes 33:** 33 topologically distinct cases (instead of 15) that guarantee
topologically correct meshes.

---

## 7. 2D Version: Marching Squares

The 2D analog: extract contours from 2D scalar field:
- 4 corners per "square" -> 16 cases -> 4 unique cases
- Used for: contour plots, 2D segmentation boundaries
- Simple and fast: O(n) where n = number of cells

---

## 8. Variants and Extensions

| Variant | Innovation | Use Case |
|---|---|---|
| Marching Tetrahedra | Decompose cube to 6 tetrahedra; no ambiguity | Alternative to MC |
| Dual Marching Cubes | Place vertices at grid centers; cleaner topology | Cleaner meshes |
| Adaptive MC | Non-uniform grids (octree) for efficiency | Large volumes |
| METABALLS | MC applied to implicit potential fields | 3D modeling |
| GPU-accelerated MC | Parallel execution on CUDA/OpenCL | Real-time reconstruction |

---

## 9. Medical Imaging Pipeline

```
CT/MRI scanner
    |
    v
DICOM files (512x512 x N slices, 16-bit integers)
    |
    v
Preprocessing (gaussian smoothing, resampling)
    |
    v
Segmentation (thresholding, U-Net, etc.)
    |
    v
MARCHING CUBES at isovalue=0.5
    |
    v
Triangle mesh (STL, OBJ format)
    |
    v
Post-processing (smoothing, simplification)
    |
    v
Visualization / 3D printing / Surgery planning
```

---

## 10. Performance

- Time complexity: O(V) where V = number of voxels
- Space: O(E) output triangles, E ~ V in practice
- Typical: 512^3 volume processed in ~1 second on modern CPU
- GPU: Real-time for 256^3 volumes

---

*Sources: Wikipedia Marching cubes; Lorensen & Cline SIGGRAPH 1987; Chernyaev MC33 1995*
