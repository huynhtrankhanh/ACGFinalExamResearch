# Bezier Surfaces --- Complete Reference

## 1. Definition

A Bezier surface of degree (m,n) is defined by an (m+1)x(n+1) grid of control points P_{i,j}:

```
           m    n
B(u,v) =  Sum  Sum  B_{i,m}(u) * B_{j,n}(v) * P_{i,j}
          i=0  j=0
```

This is a TENSOR PRODUCT surface: independently apply the 1D Bezier formula in u-direction
and v-direction.

u in [0,1], v in [0,1]

---

## 2. Bicubic Bezier Patch (Most Important)

Degree (3,3): 4x4 = 16 control points

```
B(u,v) = Sum_{i=0}^{3} Sum_{j=0}^{3}  B_{i,3}(u) * B_{j,3}(v) * P_{i,j}
```

Control point grid:
```
P00  P01  P02  P03
P10  P11  P12  P13
P20  P21  P22  P23
P30  P31  P32  P33
```

The FOUR CORNER POINTS (P00, P03, P30, P33) lie ON the surface.
All other points are off-surface "handles".

---

## 3. How to Evaluate B(u,v) --- Two-Stage Method

### Stage 1: Fix v, evaluate each ROW as a Bezier curve in v

For each row i=0,1,...,m:
```
Q_i(v) = Sum_{j=0}^{n} B_{j,n}(v) * P_{i,j}
```
This gives m+1 new "row-reduced" control points Q_0(v), Q_1(v), ..., Q_m(v)

### Stage 2: Evaluate the result as a Bezier curve in u

```
B(u,v) = Sum_{i=0}^{m} B_{i,m}(u) * Q_i(v)
```

### KEY: You can do Stage 1 and Stage 2 in either order (u then v, or v then u)!

---

## 4. Full Worked Example: Bilinear Patch (degree 1,1)

4 control points:
```
P00=(0,0,0)   P01=(1,0,1)
P10=(0,1,1)   P11=(1,1,0)
```

Evaluate at (u,v) = (0.5, 0.5):

**Stage 1 (fix u=0.5, evaluate rows in u-direction... or v-direction first):**

Actually let us fix v=0.5 and evaluate each row in v:
```
Q0(0.5) = B_{0,1}(0.5)*P00 + B_{1,1}(0.5)*P01
        = 0.5*(0,0,0) + 0.5*(1,0,1)
        = (0.5, 0, 0.5)

Q1(0.5) = 0.5*P10 + 0.5*P11
        = 0.5*(0,1,1) + 0.5*(1,1,0)
        = (0.5, 1.0, 0.5)
```

**Stage 2 (evaluate Q0, Q1 in u at u=0.5):**
```
B(0.5,0.5) = 0.5*Q0(0.5) + 0.5*Q1(0.5)
           = 0.5*(0.5,0,0.5) + 0.5*(0.5,1,0.5)
           = (0.25,0,0.25) + (0.25,0.5,0.25)
           = (0.5, 0.5, 0.5)
```

ANSWER: B(0.5,0.5) = (0.5, 0.5, 0.5) -- center of patch.

---

## 5. Full Worked Example: Biquadratic Patch (degree 2,2)

9 control points (3x3 grid):
```
Row 0 (i=0): P00=(0,0,0)  P01=(1,0,1)  P02=(2,0,0)
Row 1 (i=1): P10=(0,1,1)  P11=(1,1,2)  P12=(2,1,1)
Row 2 (i=2): P20=(0,2,0)  P21=(1,2,1)  P22=(2,2,0)
```

Evaluate at (u,v) = (0.5, 0.5):

Bernstein quadratic at t=0.5: B_{0,2}=0.25, B_{1,2}=0.50, B_{2,2}=0.25

**Stage 1: Fix v=0.5, evaluate each row in v:**

Row 0: Q0 = 0.25*(0,0,0) + 0.50*(1,0,1) + 0.25*(2,0,0)
           = (0,0,0)+(0.5,0,0.5)+(0.5,0,0) = (1.0, 0.0, 0.5)

Row 1: Q1 = 0.25*(0,1,1) + 0.50*(1,1,2) + 0.25*(2,1,1)
           = (0,0.25,0.25)+(0.5,0.5,1.0)+(0.5,0.25,0.25) = (1.0, 1.0, 1.5)

Row 2: Q2 = 0.25*(0,2,0) + 0.50*(1,2,1) + 0.25*(2,2,0)
           = (0,0.5,0)+(0.5,1,0.5)+(0.5,0.5,0) = (1.0, 2.0, 0.5)

**Stage 2: Evaluate Q0,Q1,Q2 in u at u=0.5:**

B(0.5,0.5) = 0.25*Q0 + 0.50*Q1 + 0.25*Q2
           = 0.25*(1,0,0.5) + 0.50*(1,1,1.5) + 0.25*(1,2,0.5)
           = (0.25,0,0.125) + (0.5,0.5,0.75) + (0.25,0.5,0.125)
           = (1.0, 1.0, 1.0)

ANSWER: B(0.5,0.5) = (1, 1, 1)

---

## 6. Properties

| Property | Explanation |
|---|---|
| Corner interpolation | P00,P0n,Pm0,Pmn lie ON the surface |
| Boundary curves | Each boundary is a Bezier curve using boundary row/column |
| Tangent at (0,0) in u | partial B/partial u = m*(P10 - P00) |
| Tangent at (0,0) in v | partial B/partial v = n*(P01 - P00) |
| Normal at corner | (partial u) x (partial v) |
| Convex hull | Entire surface lies in convex hull of all control points |
| Affine invariance | Transform control points = transform surface |

---

## 7. Partial Derivatives for Surface Normals

For bicubic (m=n=3):

partial B/partial u (u,v) = 3 * Sum_{i=0}^{2} Sum_{j=0}^{3} B_{i,2}(u)*B_{j,3}(v)*(P_{i+1,j}-P_{i,j})
partial B/partial v (u,v) = 3 * Sum_{i=0}^{3} Sum_{j=0}^{2} B_{i,3}(u)*B_{j,2}(v)*(P_{i,j+1}-P_{i,j})

Surface normal: N = (partial B/partial u) x (partial B/partial v)

---

## 8. Extensions

- **Bezier Triangle**: Triangular domain, barycentric coordinates
- **NURBS**: Non-Uniform Rational B-Splines = weighted control points with knot vectors; generalizes Bezier surfaces; industry standard in CAD (AutoCAD, CATIA, SolidWorks)
- **Subdivision Surfaces**: Catmull-Clark, Loop -- refine control mesh toward smooth limit surface; used in Pixar/DreamWorks animation, game characters

---
*Sources: Wikipedia Bezier surface; Farin 'Curves and Surfaces for CAGD'; Shirley 'Fundamentals of Computer Graphics'*
