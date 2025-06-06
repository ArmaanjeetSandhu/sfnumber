from core import SigFigNumber

# Demonstration and Testing
print("=== SigFigNumber Class Demonstration ===\n")

# 1. Creating numbers from strings (automatic sig fig detection)
print("1. Creating numbers from strings:")
num1 = SigFigNumber("123.45")
num2 = SigFigNumber("0.00456")
num3 = SigFigNumber("1200")
num4 = SigFigNumber("1.20e3")

print(f"'123.45' -> {num1}")
print(f"'0.00456' -> {num2}")
print(f"'1200' -> {num3}")
print(f"'1.20e3' -> {num4}")

# 2. Creating numbers with explicit significant figures
print("\n2. Creating numbers with explicit sig figs:")
num5 = SigFigNumber(1200, sigfigs=2)
num6 = SigFigNumber(1200, sigfigs=4)
print(f"1200 with 2 sig figs -> {num5}")
print(f"1200 with 4 sig figs -> {num6}")

# 3. Multiplication and Division (min sig figs rule)
print("\n3. Multiplication and Division:")
a = SigFigNumber("25.3")  # 3 sig figs
b = SigFigNumber("4.567")  # 4 sig figs
print(f"{a} × {b} = {a * b}")
print(f"{b} ÷ {a} = {b / a}")

# 4. Addition and Subtraction (decimal places rule)
print("\n4. Addition and Subtraction:")
c = SigFigNumber("123.4")  # 1 decimal place
d = SigFigNumber("5.678")  # 3 decimal places
print(f"{c} + {d} = {c + d}")
print(f"{c} - {d} = {c - d}")

# 5. Mixed operations
print("\n5. Mixed operations:")
x = SigFigNumber("2.50")  # 3 sig figs
y = SigFigNumber("3.7")  # 2 sig figs
z = SigFigNumber("10.05")  # 4 sig figs

result1 = x * y
result2 = result1 + z
print(f"({x} × {y}) = {result1}")
print(f"{result1} + {z} = {result2}")

# 6. Scientific notation handling
print("\n6. Scientific notation:")
sci1 = SigFigNumber("6.02e23")  # Avogadro's number
sci2 = SigFigNumber("1.66e-27")  # Proton mass
print(f"Avogadro's number: {sci1}")
print(f"Proton mass: {sci2}")
print(f"Product: {sci1 * sci2}")

# 7. Edge cases
print("\n7. Edge cases:")
small = SigFigNumber("0.0001234")
large = SigFigNumber("9876543")
print(f"Very small: {small}")
print(f"Very large: {large}")
print(f"Small × Large: {small * large}")

# 8. Practical chemistry example
print("\n8. Practical chemistry example:")
print("Calculating molarity: moles / volume")
moles = SigFigNumber("0.0456")  # 3 sig figs
volume = SigFigNumber("0.250")  # 3 sig figs
molarity = moles / volume
print(f"Moles: {moles}")
print(f"Volume (L): {volume}")
print(f"Molarity (M): {molarity}")

# 9. Testing with regular Python numbers
print("\n9. Operations with regular numbers:")
sig_num = SigFigNumber("45.6")
regular_num = 2
print(f"{sig_num} × {regular_num} = {sig_num * regular_num}")
print(f"{regular_num} × {sig_num} = {regular_num * sig_num}")  # Tests __rmul__
