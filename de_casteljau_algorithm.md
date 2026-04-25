# De Casteljau's Algorithm --- Complete Guide

> Wikipedia says: "De Casteljau's algorithm is a recursive method to evaluate polynomials in Bernstein form or Bezier curves, named after its inventor Paul de Casteljau. The algorithm is numerically stable compared to direct evaluation of polynomials. The computational complexity is O(dn^2) where d is the number of dimensions and n is the number of control points."

---

## 1. Why Use De Casteljau?

**Problem:** Direct evaluation of B(t) = Sum C(n,i)*t^i*(1-t)^(n-i)*Pi requires computing large powers (t^n) and binomial coefficients, which can cause numerical overflow/precision loss for high n.

**Solution:** De Casteljau's algorithm uses only linear interpolation at each step --- a convex combination (weights sum to 1, both non-negative). This guarantees numerical stability because intermediate points always stay within the convex hull.

---

## 2. The Algorithm

### Initialize (Level 0):
```
P_i^(0) = P_i    for i = 0, 1, ..., n
```

### Recurrence (n rounds):
```
P_i^(j) = (1-t0) * P_i^(j-1)  +  t0 * P_(i+1)^(j-1)
```
for j = 1, 2, ..., n and i = 0, 1, ..., n-j

### Result:
```
B(t0) = P_0^(n)
```

The key recurrence boxed:
```
┌──────────────────────────────────────────────────────────┐
│  P_i^(j) = (1-t) * P_i^(j-1)  +  t * P_(i+1)^(j-1)    │
└──────────────────────────────────────────────────────────┘
```

---

## 3. Triangle Scheme for Hand Computation

This is how to organize your work on paper. Draw a triangle and fill left-to-right:

```
Level j=0    j=1       j=2       j=3
─────────────────────────────────────────────────────
P0^(0)
           P0^(1)
P1^(0)               P0^(2)
           P1^(1)               P0^(3)  <-- ANSWER
P2^(0)               P1^(2)
           P2^(1)
P3^(0)
```

**Each entry = (1-t) * entry_above_left  +  t * entry_below_left**

For a QUADRATIC (3 points, 2 rounds):
```
P0^(0)
           P0^(1)
P1^(0)               P0^(2)  <-- ANSWER
           P1^(1)
P2^(0)
```

---

## 4. Complete Worked Examples

### Example A: Quadratic at t = 0.5

Given: P0=(0,0), P1=(2,4), P2=(4,0)

```
Level 0:  (0,0)      (2,4)      (4,0)

Level 1:
  Q0 = 0.5*(0,0) + 0.5*(2,4) = (0,0)+(1,2) = (1, 2)
  Q1 = 0.5*(2,4) + 0.5*(4,0) = (1,2)+(2,0) = (3, 2)

Level 2:
  R0 = 0.5*(1,2) + 0.5*(3,2) = (0.5,1)+(1.5,1) = (2, 2)

ANSWER: B(0.5) = (2, 2)
```

Verify: (1/4)(0,0) + (2/4)(2,4) + (1/4)(4,0) = (0+1+1, 0+2+0) = (2,2) CORRECT

---

### Example B: Quadratic at t = 3/4

Given: P0=(0,0), P1=(1,2), P2=(3,0)

**t=0.75, (1-t)=0.25**

```
Level 0:  (0,0)      (1,2)      (3,0)

Level 1:
  Q0 = 0.25*(0,0) + 0.75*(1,2) = (0,0)+(0.75,1.5) = (0.75, 1.5)
  Q1 = 0.25*(1,2) + 0.75*(3,0) = (0.25,0.5)+(2.25,0) = (2.5, 0.5)

Level 2:
  R0 = 0.25*(0.75,1.5) + 0.75*(2.5,0.5)
     = (0.1875, 0.375) + (1.875, 0.375)
     = (2.0625, 0.75)

ANSWER: B(0.75) = (2.0625, 0.75) = (33/16, 3/4)
```

---

### Example C: Cubic at t = 0.5

Given: P0=(0,0), P1=(0,1), P2=(1,1), P3=(1,0)

**t=0.5, (1-t)=0.5**

```
Level 0:  (0,0)     (0,1)     (1,1)     (1,0)

Level 1:
  Q0 = 0.5*(0,0)+0.5*(0,1) = (0, 0.5)
  Q1 = 0.5*(0,1)+0.5*(1,1) = (0.5, 1.0)
  Q2 = 0.5*(1,1)+0.5*(1,0) = (1.0, 0.5)

Level 2:
  R0 = 0.5*(0,0.5)+0.5*(0.5,1.0) = (0.25, 0.75)
  R1 = 0.5*(0.5,1.0)+0.5*(1.0,0.5) = (0.75, 0.75)

Level 3:
  S0 = 0.5*(0.25,0.75)+0.5*(0.75,0.75) = (0.5, 0.75)

ANSWER: B(0.5) = (0.5, 0.75)
```

---

### Example D: Cubic at t = 1/3

Given: P0=(0,0), P1=(3,0), P2=(3,3), P3=(0,3)

**t=1/3, (1-t)=2/3**

```
Level 0:  (0,0)    (3,0)    (3,3)    (0,3)

Level 1:
  Q0 = (2/3)(0,0) + (1/3)(3,0) = (0,0)+(1,0)   = (1, 0)
  Q1 = (2/3)(3,0) + (1/3)(3,3) = (2,0)+(1,1)   = (3, 1)
  Q2 = (2/3)(3,3) + (1/3)(0,3) = (2,2)+(0,1)   = (2, 3)

Level 2:
  R0 = (2/3)(1,0) + (1/3)(3,1) = (2/3+1, 0+1/3) = (5/3, 1/3)
  R1 = (2/3)(3,1) + (1/3)(2,3) = (2+2/3, 2/3+1) = (8/3, 5/3)

Level 3:
  S0 = (2/3)(5/3,1/3) + (1/3)(8/3,5/3)
     = (10/9+8/9, 2/9+5/9)
     = (18/9, 7/9) = (2, 7/9)

ANSWER: B(1/3) = (2, 7/9) ≈ (2.0, 0.778)
```

---

### Example E: Degree-5 (Quintic) at t = 0.5

Given: P0=(0,0), P1=(1,2), P2=(2,4), P3=(3,4), P4=(4,2), P5=(5,0)

**t=0.5, all weights 0.5**

```
Level 0:  (0,0) (1,2) (2,4) (3,4) (4,2) (5,0)

Level 1 [each pair avg]:
  (0.5,1) (1.5,3) (2.5,4) (3.5,3) (4.5,1)

Level 2 [each pair avg]:
  (1,2) (2,3.5) (3,3.5) (4,2)

Level 3 [each pair avg]:
  (1.5,2.75) (2.5,3.5) (3.5,2.75)

Level 4 [each pair avg]:
  (2,3.125) (3,3.125)

Level 5 [final avg]:
  (2.5, 3.125)

ANSWER: B(0.5) = (2.5, 3.125)
```

---

## 5. Mental Math Shortcuts

**For t = 0.5:** Every step is just averaging adjacent pairs. Fastest computation.

**For t = 1/3:** Use fractions 2/3 and 1/3. Keep exact fractions throughout.

**For t = 3/4:** Use fractions 1/4 and 3/4. Denominators build up as powers of 4.

**Check:** At t=0 the answer should be P0; at t=1 it should be Pn. Use this to verify direction.

---

## 6. Common Mistakes

1. **Wrong order of blending:** It's (1-t)*left + t*right, NOT t*left + (1-t)*right
2. **Forgetting to do n rounds:** n+1 points needs n rounds (a cubic with 4 points needs 3 rounds)
3. **Wrong triangle structure:** Each round has one fewer point than the previous
4. **Not verifying at t=0 or t=1:** Quick sanity check

---

*Sources: Wikipedia De Casteljau's algorithm; Paul de Casteljau's original 1959 report at Citroen*
