from core import SigFigNumber

print("=== Sig Fig Counting Tests ===")
test_cases = [
    ("123", 3),
    ("123.0", 4),
    ("123.00", 5),
    ("0.00123", 3),
    ("1.200", 4),
    ("1200", 4),  # Ambiguous case
    ("1.23e4", 3),
]

for value, expected in test_cases:
    num = SigFigNumber(value)
    print(f"{value} -> {num.sigfigs} sig figs (expected {expected})")

print("\n=== Arithmetic Tests ===")
a = SigFigNumber("12.3")  # 3 sig figs
b = SigFigNumber("4.56")  # 3 sig figs
c = SigFigNumber("1.2")  # 2 sig figs

print(f"a = {a}")
print(f"b = {b}")
print(f"c = {c}")
print(f"a * c = {a * c}")  # Should have 2 sig figs
print(f"a / c = {a / c}")  # Should have 2 sig figs
print(f"a + b = {a + b}")  # Should have 1 decimal place
print(f"a - b = {a - b}")  # Should have 1 decimal place
