# Part C: Interview Ready

---

## Q1 — `elif` vs Multiple `if` Statements

### The Core Difference

`elif` is a **chain** — only one block ever runs, the first match wins,
and the rest are skipped entirely.

Multiple `if` statements are **independent** — Python checks every single
one, regardless of what matched before.

### Example Where They Produce Different Output

**Input:** `score = 85`

---

**Using multiple `if` (WRONG for grading):**
```python
score = 85

if score >= 60:
    grade = 'D'
if score >= 70:
    grade = 'C'
if score >= 80:
    grade = 'B'
if score >= 90:
    grade = 'A'

print(grade)
```
**Output:** `B`

Why? All four `if` conditions are checked independently:
- `85 >= 60` → grade = 'D'
- `85 >= 70` → grade = 'C' (overwrites D)
- `85 >= 80` → grade = 'B' (overwrites C)
- `85 >= 90` → skipped

The final value of `grade` is whatever the **last matching `if`** set it to.

---

**Using `elif` (CORRECT for grading):**
```python
score = 85

if score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B'
elif score >= 70:
    grade = 'C'
elif score >= 60:
    grade = 'D'
else:
    grade = 'F'

print(grade)
```
**Output:** `B`

Why? Python checks top-down:
- `85 >= 90` → skip
- `85 >= 80` → grade = 'B' → **STOP, no more checks**

### When to use which

Use `elif` when conditions are **mutually exclusive** (grades, categories,
menus). Use multiple `if` when conditions are **independent** and you want
all matching ones to run (e.g., applying multiple discounts to an order).

---

## Q2 — Triangle Classifier
```python
"""Triangle classification module."""


def classify_triangle(a, b, c):
    """
    Classify a triangle based on its three sides.

    Args:
        a (float): First side length.
        b (float): Second side length.
        c (float): Third side length.

    Returns:
        str: Triangle type or reason it is invalid.
    """
    # Edge case: zero or negative sides
    if a <= 0 or b <= 0 or c <= 0:
        return "Invalid — sides must be positive numbers."

    # Triangle inequality rule: each side must be less than sum of other two
    if a >= b + c or b >= a + c or c >= a + b:
        return "Not a triangle — one side is too long."

    # Classify by sides
    if a == b == c:
        return "Equilateral — all three sides are equal."
    elif a == b or b == c or a == c:
        return "Isosceles — two sides are equal."
    else:
        return "Scalene — all three sides are different."


# --- Test Cases ---
print(classify_triangle(5, 5, 5))      # Equilateral
print(classify_triangle(5, 5, 3))      # Isosceles
print(classify_triangle(3, 4, 5))      # Scalene
print(classify_triangle(1, 2, 3))      # Not a triangle (1 + 2 = 3, not >)
print(classify_triangle(0, 4, 5))      # Invalid — zero side
print(classify_triangle(-1, 4, 5))     # Invalid — negative side
print(classify_triangle(10, 1, 1))     # Not a triangle
```

**Expected Output:**
```
Equilateral — all three sides are equal.
Isosceles — two sides are equal.
Scalene — all three sides are different.
Not a triangle — one side is too long.
Invalid — sides must be positive numbers.
Invalid — sides must be positive numbers.
Not a triangle — one side is too long.
```

---

## Q3 — Debug the Grade Code

### Original Buggy Code:
```python
score = 85

if score >= 60:
    grade = 'D'
if score >= 70:
    grade = 'C'
if score >= 80:
    grade = 'B'
if score >= 90:
    grade = 'A'

print(grade)
```

### What is the bug?

All four conditions use independent `if` statements instead of `elif`.
Python checks every `if` separately, so multiple conditions can match and
each one **overwrites** the `grade` variable set by the previous one.

### Why does it give wrong output?

For `score = 85`:
- `if score >= 60` → True → grade = `'D'`
- `if score >= 70` → True → grade = `'C'` (overwrites D)
- `if score >= 80` → True → grade = `'B'` (overwrites C)
- `if score >= 90` → False → skipped

Final grade is `'B'` — which happens to be correct for 85, but only by
coincidence. For `score = 95`, grade would incorrectly be set to `'A'`
only because `>= 90` is the last `if` that fires. The logic is fragile
and wrong in design even when it produces the right answer.

Try `score = 95`:
- All four `if` blocks fire in sequence
- grade ends as `'A'` — correct by accident, not by design

Try `score = 72`:
- `>= 60` grade = D
- `>= 70` grade = C (overwrites — should have stopped here!)
- `>= 80` 
- `>= 90` 
- Prints `'C'` — correct again by coincidence, but logic is still broken

### Correct Fix:
```python
score = 85

if score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B'
elif score >= 70:
    grade = 'C'
elif score >= 60:
    grade = 'D'
else:
    grade = 'F'

print(grade)
```

**Key fix:** Changed all `if` to `elif` (except the first) and reversed
the order to check highest first. Now exactly one block ever runs.
