## Dot Product of Two Vectors

The dot product of two vectors `a` and `b` (sometimes called the *inner product*, or, since its result is a scalar, the *scalar product*) is denoted by `a · b`, and is defined as

```
a · b = |a| × |b| × cos(θ)
```

where θ is the measure of the angle between `a` and `b` (see trigonometric function for an explanation of cosine).

Geometrically, this means that `a` and `b` are drawn with a common start point, and then the length of `a` is multiplied with the *length of the component of* `b` *that points in the same direction as* `a`.

The dot product can also be defined as the sum of the products of the components of each vector as


Let `a` and `b` be two vectors in 3D space:

Vector `a = (a₁, a₂, a₃)`

Vector `b = (b₁, b₂, b₃)`


The *dot product* by definition is:

```
a · b = a₁b₁ + a₂b₂ + a₃b₃
```

Let's derive the relationship with the magnitudes and angle.

### Step 1

Consider the Law of Cosines for the triangle formed by vectors `a, b,` and `(a - b)`.

```
|a - b|² = |a|² + |b|² - 2|a||b|cos(θ)
```

### Step 2

Expand `|a - b|²` using the dot product definition:

```
|a - b|² = (a - b)·(a - b)
= (a₁-b₁)² + (a₂-b₂)² + (a₃-b₃)²
= a₁² + a₂² + a₃² + b₁² + b₂² + b₃² - 2(a₁b₁ + a₂b₂ + a₃b₃)
= |a|² + |b|² - 2(a·b)
```

### Step 3

Equate the two expressions for `|a - b|²`
```
|a|² + |b|² - 2(a·b) = |a|² + |b|² - 2|a||b|cos(θ)
```

### Step 4 - Simplify
It is clear from the above step that
```
-2(a·b) = -2|a||b|cos(θ)
```

Therefore:
```
a · b = |a| × |b| × cos(θ)
```

This is the relationship between the *dot product* and the *magnitudes* of vectors and the angle between them.

It holds true for vectors in any dimension.
