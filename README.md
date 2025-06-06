## 🔹 **1. What Are Significant Figures?**

**Significant figures** are the digits in a number that carry meaning contributing to its measurement precision. They’re a way of expressing **how sure** we are about a value — essentially, how many digits in a number are **reliable**.

## 🔹 **2. Why Do They Matter?**

In any real-world measurement:

- You can never measure **perfectly** — tools have limits.
- Significant figures help preserve **uncertainty** through calculations.
- They prevent over-representing the precision of your data.

**Example:**

> If your scale only measures to the nearest gram, writing "3.0000 g" is **lying**. Just write "3 g" — that's all you're certain about.

## 🔹 **3. Rules for Identifying Significant Figures**

Here’s how to count them:

### ✅ Always Significant:

1. **Non-zero digits**
   → `345` → 3 sig figs
2. **Zeros between non-zero digits (captive zeros)**
   → `304` → 3 sig figs
   → `20.03` → 4 sig figs
3. **Trailing zeros in a decimal**
   → `12.300` → 5 sig figs
   → `0.0400` → 3 sig figs

### ❌ Not Significant:

4. **Leading zeros** (zeros in front of non-zero digits)
   → `0.00456` → 3 sig figs (just `456`)
5. **Trailing zeros in whole numbers without a decimal**
   → `1500` → _ambiguous_

   - Could be 2, 3, or 4 sig figs depending on context
   - `1.5 × 10³` → 2 sig figs
   - `1.500 × 10³` → 4 sig figs
   - Add a decimal if you want to make zeros significant: `1500.` → 4 sig figs

## 🔹 **4. Scientific Notation & Sig Figs**

Scientific notation is your best friend for clarity:

- `4.00 × 10²` → 3 sig figs
- `5.0000 × 10⁴` → 5 sig figs

Always count the digits in the **coefficient** (the part before ×10^n).

## 🔹 **5. Rounding with Significant Figures**

### General rules:

- **Look at the digit after your last desired sig fig:**

  - If < 5 → round down
  - If ≥ 5 → round up

> Example: Round `3.476` to 3 sig figs → `3.48`
> Example: Round `5.4449` to 3 sig figs → `5.44`

> ⚠️ Rounding should happen **only at the end** of multi-step calculations, unless specified otherwise. Don’t round prematurely — you’ll introduce compounding errors.

## 🔹 **6. Sig Figs in Mathematical Operations**

### ➕ Addition/Subtraction:

- The **decimal place** controls sig figs.
- Result should have as many **decimal places** as the number with the **least** decimal places.

> `12.11 + 0.3 = 12.41` → round to `12.4`

### ✖️ Multiplication/Division:

- The **number of sig figs** controls the result.
- Final result has as many **sig figs** as the input with the **least sig figs**.

> `3.44 × 2.1 = 7.224` → round to `7.2`

## 🔹 **7. Exact Numbers**

Some numbers have **infinite** sig figs:

- Definitions: `1 inch = 2.54 cm (exact)`
- Counts: `3 apples`, `12 students`

These do **not** limit the number of significant figures in calculations.

## 🔹 **8. Common Mistakes**

- Rounding **too early**
- Assuming trailing zeros in whole numbers are significant
- Ignoring that the **type of operation** affects how you round
- Not using **scientific notation** for clarity in ambiguous numbers

## 🔹 **9. Real-World Example**

Let’s say:

- You measure a length: `3.45 m` (3 sig figs)
- Another length: `1.2 m` (2 sig figs)
- Multiply them to find area:

→ `3.45 × 1.2 = 4.14 m²`
→ Round to **2 sig figs**: `4.1 m²`

If you kept all digits (`4.1400 m²`), you're misrepresenting precision — implying you're sure down to 0.0001 m², which you’re not.

## 🔹 **10. Sig Figs in Engineering / Programming / Lab Reports**

- **In engineering:** Overstating precision is a red flag.
- **In code:** Floating point variables do not “store” sig figs, but you can format output to match them.
- **In lab reports:** Sig figs reflect your instrument accuracy — always match them unless the protocol says otherwise.

## 🔹 **11. Summary Cheat Sheet**

| Type                      | Rule                          | Example              | Sig Figs |
| ------------------------- | ----------------------------- | -------------------- | -------- |
| Non-zero digits           | Always                        | `456`                | 3        |
| Captive zeros             | Always                        | `405`                | 3        |
| Leading zeros             | Never                         | `0.0034`             | 2        |
| Trailing zeros w/ decimal | Always                        | `2.300`              | 4        |
| Trailing zeros no decimal | Unclear                       | `1500`               | 2–4?     |
| Addition/Subtraction      | Round to least decimal places | `3.45 + 1.2` → `4.7` |          |
| Multiplication/Division   | Round to fewest sig figs      | `2.5 × 3.42` → `8.6` |          |

## 🔸 **12. Significant Figures vs Decimal Places (Deep Clarification)**

These are **not** the same:

- **Decimal places**: Number of digits **after the decimal**
  → Used in **addition/subtraction**

- **Significant figures**: Total number of meaningful digits
  → Used in **multiplication/division**

> `0.00340` has **3 sig figs** but **5 decimal places**

## 🔸 **13. Sig Figs in Logarithms and Exponentials**

### For logs:

> `log(3.40 × 10²)` = `log(340)` ≈ `2.531`

- **Rule**: The number of **sig figs in the input** → Number of **decimal places** in the result.

→ `3.40` has 3 sig figs → result: 3 decimal places → `2.531`

### For antilogs (e.g., 10^x):

> `10^2.53` ≈ `338.84`

- **Decimal places** in exponent → **sig figs** in result.

## 🔸 **14. Sig Figs in Trig, Roots, Powers**

- **Trig functions (sin, cos, tan)**: Match sig figs to input
- **Roots & exponents**: Result matches **fewest sig figs**

> `√2.40` = `1.549` → round to `1.55` (3 sig figs)

## 🔸 **15. Repeating Calculations: Guard Digits**

When doing **multi-step calculations**, always keep **extra digits** (guard digits) until the final step.

> If you round at every step, your final answer is garbage.

## 🔸 **16. Measurement vs Counting**

- **Measurements** = subject to uncertainty → use sig figs.
- **Counting** (like 10 students) = exact → infinite sig figs.

## 🔸 **17. Sig Figs in Constants**

- Constants from tables (e.g. Planck’s constant) **have sig figs** depending on how they’re given.
- **Defined constants** (e.g. `1 mole = 6.02214076×10²³`) are often **exact** based on SI definition.

## 🔸 **18. Significant Figures in Programming/Output Formatting**

Languages like Python/C/C++ don't “store” sig figs, but you can **format** output:

### Python example:

```python
"{:.3g}".format(0.00456123)  # → '0.00456' (3 sig figs)
```

- Use `g` for sig figs, `f` for decimal places.

## 🔸 **19. Sig Figs in Error Propagation**

In experimental physics/engineering, uncertainties propagate:

If `A = 3.2 ± 0.1`, and `B = 2.0 ± 0.1`, then:

- **Addition/Subtraction**: Add **absolute errors**
- **Multiplication/Division**: Add **relative (%) errors**

Final result should be rounded so that the **uncertainty and value match in decimal place** — and then sig figs follow from there.

## 🔸 **20. Significant Figures in Graphs and Tables**

When reporting:

- Round table values consistently
- Uncertainty values should be reported with **1 or 2 sig figs**, and main values should match its decimal place

## 🔸 **21. Philosophical and Practical Limitations**

- Sig figs are an **approximation** of uncertainty handling.
- They **don't replace** error bars or standard deviation.
- In high-level research, you’ll move beyond sig figs into **uncertainty analysis**, **confidence intervals**, etc.
- Sig figs are **strictly followed in labs, reports, and exams**, but in the real world, people sometimes **ignore them** if they don’t matter for the application (e.g., in spreadsheets, dashboards).
