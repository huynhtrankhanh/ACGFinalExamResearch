# Bézier Curves — Complete Reference

> *Wikipedia says:* "A Bézier curve is a parametric curve used in computer graphics and related fields. A set of discrete 'control points' defines a smooth, continuous curve by means of a formula. The Bézier curve is named after French engineer Pierre Bézier (1910–1999), who used it in the 1960s for designing curves for the bodywork of Renault cars."

---

## 1. History

| Person | Company | Year | Contribution |
|---|---|---|---|
| Paul de Casteljau | Citroën | 1959 | Recursive algorithm (unpublished until 1980s) |
| Pierre Bézier | Renault | 1960s | Publicly described polynomial-based curves (UNISURF) |
| Sergei Bernstein | — | 1912 | Bernstein basis polynomials (mathematical foundation) |

Both de Casteljau and Bézier independently discovered the same mathematical curves built on Bernstein polynomials. The algorithm is named after de Casteljau; the curves after Bézier.

---

## 2. Bernstein Basis Polynomials

The building blocks of Bézier curves:

$$B_{i,n}(t) = \binom{n}{i} t^i (1-t)^{n-i}, \quad t \in [0,1]$$

**Key properties (MEMORIZE):**
- Sum to 1: $\sum_{i=0}^n B_{i,n}(t) = 1$
- Non-negative: $B_{i,n}(t) \geq 0$
- Maximum at $t = i/n$
- Symmetry: $B_{i,n}(t) = B_{n-i,n}(1-t)$

**Values at endpoints:**
- $B_{0,n}(0) = 1$, all others = 0 at t=0
- $B_{n,n}(1) = 1$, all others = 0 at t=1

---

## 3. The Bézier Curve Formula

$$\boxed{B(t) = \sum_{i=0}^{n} \binom{n}{i} (1-t)^{n-i} t^i \cdot P_i}$$

---

## 4. Specific Degrees

### Degree 1 (Linear) — 2 points
$$B(t) = (1-t)P_0 + t\,P_1$$

### Degree 2 (Quadratic) — 3 points
$$B(t) = (1-t)^2 P_0 + 2t(1-t)P_1 + t^2 P_2$$

**Coefficients: 1, 2, 1**

### Degree 3 (Cubic) — 4 points ★ MOST COMMON ★
$$B(t) = (1-t)^3 P_0 + 3t(1-t)^2 P_1 + 3t^2(1-t) P_2 + t^3 P_3$$

**Coefficients: 1, 3, 3, 1**

### Degree 4 (Quartic) — 5 points
$$B(t) = (1-t)^4 P_0 + 4t(1-t)^3 P_1 + 6t^2(1-t)^2 P_2 + 4t^3(1-t) P_3 + t^4 P_4$$

**Coefficients: 1, 4, 6, 4, 1**

### Degree 5 (Quintic) — 6 points
$$B(t) = (1-t)^5 P_0 + 5t(1-t)^4 P_1 + 10t^2(1-t)^3 P_2 + 10t^3(1-t)^2 P_3 + 5t^4(1-t) P_4 + t^5 P_5$$

**Coefficients: 1, 5, 10, 10, 5, 1**

---

## 5. Pascal's Triangle (Binomial Coefficients Lookup)

```
n=0:          1
n=1:        1   1
n=2:      1   2   1
n=3:    1   3   3   1
n=4:  1   4   6   4   1
n=5: 1   5  10  10   5   1
n=6: 1   6  15  20  15   6   1
```

Rule: each number = sum of two numbers directly above it.
C(n,i) = C(n-1,i-1) + C(n-1,i)

---

## 6. Properties You Must Know

| Property | Formula/Explanation |
|---|---|
| **Endpoint interpolation** | B(0)=P₀, B(1)=Pₙ always |
| **Convex hull** | Entire curve lies within convex hull of control points |
| **Affine invariance** | Transform control points → transforms curve identically |
| **Tangent at start** | B'(0) = n·(P₁ − P₀) |
| **Tangent at end** | B'(1) = n·(Pₙ − Pₙ₋₁) |
| **Derivative is Bézier** | B'(t) is a Bézier of degree n−1 with ΔPᵢ = n(Pᵢ₊₁−Pᵢ) |
| **Symmetry** | Reverse Pᵢ order → same curve reversed |

---

## 7. Derivatives

**First derivative** (itself a Bézier of degree n−1):
$$B'(t) = n \sum_{i=0}^{n-1} B_{i,n-1}(t) \cdot (P_{i+1} - P_i)$$

**Cubic first derivative** (degree 2 Bézier with ΔPs):
$$B'(t) = 3[(1-t)^2(P_1-P_0) + 2t(1-t)(P_2-P_1) + t^2(P_3-P_2)]$$

**At t=0:** $B'(0) = n(P_1 - P_0)$ (tangent direction P₀→P₁, magnitude n)
**At t=1:** $B'(1) = n(P_n - P_{n-1})$ (tangent direction Pₙ₋₁→Pₙ, magnitude n)

---

## 8. Quick Evaluation at Special t Values

### At t = 0.5
| Degree | Formula | Value |
|---|---|---|
| Linear | (P₀+P₁)/2 | midpoint |
| Quadratic | (P₀+2P₁+P₂)/4 | weighted average |
| Cubic | (P₀+3P₁+3P₂+P₃)/8 | weighted average |

### At t = 3/4 (Lecture Example)
For the degree-5 curve with points (0,0), (1,0), (2,1), (3,1), (4,0), (5,0):
Result: **B(0.75) = (3.75, 0.3515625)**
(See `de_casteljau_algorithm.md` for full calculation)

### At t = 1/3
Coefficients for quadratic: (1-1/3)²=4/9, 2(1/3)(2/3)=4/9, (1/3)²=1/9
$$B(1/3) = \frac{4}{9}P_0 + \frac{4}{9}P_1 + \frac{1}{9}P_2$$

### At t = 3/4 = 0.75
Coefficients for quadratic: (1/4)²=1/16, 2(3/4)(1/4)=6/16, (3/4)²=9/16
$$B(3/4) = \frac{1}{16}P_0 + \frac{6}{16}P_1 + \frac{9}{16}P_2$$

---

## 9. Applications

- **Adobe Illustrator / Inkscape / SVG**: All paths are cubic Bézier splines
- **TrueType fonts**: Quadratic Béziers for glyph outlines
- **OpenType/PostScript fonts**: Cubic Béziers
- **CSS animations**: `cubic-bezier(p1x, p1y, p2x, p2y)` controls timing
- **Computer-aided design (CAD)**: Foundation of NURBS (Non-Uniform Rational B-Splines)
- **CNC machining**: Tool path generation
- **Robotics**: Smooth trajectory planning
- **Games**: Camera paths, character animations, UI transitions

---

## 10. Relationship to Other Splines

| Spline Type | Based On | Properties |
|---|---|---|
| Bézier | Bernstein polynomials | Global control (moving any point affects whole curve) |
| B-Spline | B-spline basis | Local control; pieces share knot vectors |
| NURBS | Rational B-Splines | Exact conics (circles, ellipses); industry standard |
| Hermite | Positions + tangents | Interpolates endpoints AND tangents |
| Catmull-Rom | 4 nearby points | Passes through all control points (interpolating) |

---

*Sources: Wikipedia Bézier curve article; Farin, "Curves and Surfaces for CAGD" (Morgan Kaufmann); Shirley, "Fundamentals of Computer Graphics"*
