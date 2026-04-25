# Delaunay Triangulation --- Complete Guide

> Wikipedia says: "A Delaunay triangulation of a set of points in the plane subdivides their convex hull into triangles whose circumcircles do not contain any of the points. This maximizes the size of the smallest angle in any of the triangles, and tends to avoid sliver triangles."
> Named after Boris Delaunay for his work from 1934.

---

## 1. The Core Definition

**Circumcircle Property:** For every triangle in the Delaunay triangulation, the circumcircle (the unique circle passing through all 3 vertices) contains NO other input point in its interior.

If any point P lies inside the circumcircle of triangle ABC, then ABC is NOT a valid Delaunay triangle and must be "flipped."

### The Circumcircle Test (Determinant)

Given triangle A,B,C (counterclockwise) and test point D:

```
|Ax-Dx  Ay-Dy  (Ax-Dx)^2+(Ay-Dy)^2|
|Bx-Dx  By-Dy  (Bx-Dx)^2+(By-Dy)^2| > 0  =>  D is INSIDE circumcircle
|Cx-Dx  Cy-Dy  (Cx-Dx)^2+(Cy-Dy)^2|
```

If determinant > 0: D inside circle => NOT Delaunay => flip edge
If determinant < 0: D outside circle => OK
If determinant = 0: D ON circle => ambiguous (degenerate)

---

## 2. Key Properties

1. **Maximizes minimum angle** -- the "fattest" triangles possible
2. **Avoids slivers** -- no long thin triangles (numerically bad for FEA, rendering)
3. **Unique** -- for n points in general position (no 4 points cocircular)
4. **Dual of Voronoi diagram** -- connect circumcenters of adjacent triangles => Voronoi edges
5. **Count** -- at most 2n-h-2 triangles (n=points, h=convex hull vertices)
6. **Geometric spanner** -- shortest path along edges is at most 1.998x Euclidean distance

---

## 3. Voronoi Duality

Voronoi cell of point p = region closer to p than any other point.

**Delaunay <-> Voronoi duality:**
- Delaunay vertex = Voronoi cell center
- Delaunay edge AB = dual Voronoi edge (perpendicular bisector of AB between Vor(A) and Vor(B))
- Delaunay triangle circumcenter = Voronoi vertex

Building one from the other is O(n) after first construction.

---

## 4. The Edge Flip Operation

Given two triangles sharing edge BD (forming quadrilateral ABCD):
- If the sum of opposite angles alpha + gamma > 180 degrees, edge BD is "illegal"
- Flip BD to AC => creates two new triangles that satisfy Delaunay condition

```
Before flip:           After flip:
    A                      A
   /|\                    /|
  / | \                  / |
 /  BD  \               /  |
B---+---C    =>      B  AC  C
 \  |  /               \  |
  \ | /                 \ |
   \|/                   \|
    D                      D
```

---

## 5. Bowyer-Watson Algorithm (O(n log n))

The most commonly implemented Delaunay triangulation algorithm:

```
Algorithm Bowyer-Watson(points):
1. Create super-triangle S that contains all input points
2. triangulation = {S}

3. For each point p in points:
   a. Find all triangles whose circumcircle contains p:
      bad_triangles = {T in triangulation : p inside circumcircle(T)}
   
   b. Find boundary polygon (hole boundary):
      boundary = edges of bad_triangles that are not shared by 2 bad triangles
   
   c. Remove bad_triangles from triangulation
   
   d. For each edge (a,b) in boundary:
      Add new triangle (a, b, p) to triangulation

4. Remove all triangles sharing a vertex with super-triangle S
5. Return triangulation
```

**Complexity:** O(n log n) expected; O(n^2) worst case

---

## 6. 3D Extension: Tetrahedralization

In 3D, Delaunay triangulation becomes Delaunay tetrahedralization:
- Instead of circumcircles, use circumspheres
- No point inside any tetrahedron's circumsphere
- Used for finite element mesh generation (FEM)
- Libraries: TetGen, CGAL, Qhull

---

## 7. Applications in Computer Graphics

| Application | Why Delaunay |
|---|---|
| Point cloud triangulation | Connect nearby points without sliver triangles |
| Terrain meshing (DEMs) | Triangulate elevation data for terrain rendering |
| Finite element analysis | Well-shaped triangles for numerical stability |
| Voronoi diagrams | Dual graph for nearest-neighbor queries |
| Path planning | Visibility graph through triangulation |
| Interpolation | Natural neighbor interpolation on Delaunay mesh |
| 2D physics simulation | Good mesh for rigid body simulation |

---

## 8. Limitations and Extensions

**Limitations:**
- Does not work well with sharp features (edges, corners) -- quality near boundary can be poor
- Assumes points in general position (no 4 cocircular points)

**Extensions:**
- **Constrained Delaunay:** Some edges are forced (e.g., known boundaries); used for terrain with roads, coastlines
- **Conforming Delaunay:** Add extra Steiner points to make triangulation conform to input edges
- **Weighted Delaunay:** Each point has a weight; circumcircle test uses weighted circles
- **Delaunay refinement (Ruppert's algorithm):** Adds vertices to improve triangle quality (minimum angle >= 20.7 degrees guaranteed)

---

*Sources: Wikipedia Delaunay triangulation; de Berg et al. 'Computational Geometry'; O'Rourke 'Computational Geometry in C'*
