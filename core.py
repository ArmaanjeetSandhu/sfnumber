import math
import re


class SigFigNumber:
    def __init__(self, value, sigfigs=None):
        if isinstance(value, str):
            self.value = float(value)
            self.sigfigs = self._count_sig_figs(value) if sigfigs is None else sigfigs
        elif isinstance(value, (int, float)):
            self.value = float(value)
            self.sigfigs = (
                sigfigs
                if sigfigs is not None
                else self._infer_sigfigs_from_float(value)
            )
        else:
            raise TypeError("Unsupported type for SigFigNumber.")

    def __repr__(self):
        return f"{self._rounded_str()} (±{self.sigfigs} sf)"

    def _rounded_str(self):
        return self._format_to_sig_figs(self.value, self.sigfigs)

    def _format_to_sig_figs(self, x, sigfigs):
        if x == 0:
            return "0"

        # Handle negative numbers
        sign = "-" if x < 0 else ""
        x = abs(x)

        # Find the order of magnitude
        order = math.floor(math.log10(x))

        # Scale the number to have the first significant digit in the ones place
        scaled = x / (10**order)

        # Round to the desired number of significant figures
        rounded_scaled = round(scaled, sigfigs - 1)

        # Scale back
        result = rounded_scaled * (10**order)

        # Format appropriately
        if order >= 0 and order < sigfigs:
            # Use fixed-point notation
            decimals = max(0, sigfigs - order - 1)
            return f"{sign}{result:.{decimals}f}"
        else:
            # Use scientific notation for very large or very small numbers
            return f"{sign}{rounded_scaled:.{sigfigs - 1}f}e{order:+d}"

    def _count_sig_figs(self, s):
        s = s.strip().lower()

        # Handle scientific notation
        if "e" in s:
            mantissa = s.split("e")[0]
            return self._count_sig_figs(mantissa)

        # Remove sign
        s = re.sub(r"^[+-]", "", s)

        if "." in s:
            # For decimal numbers
            integer_part, decimal_part = s.split(".")

            # Remove leading zeros from integer part
            integer_part = integer_part.lstrip("0")

            if integer_part:
                # If there's a non-zero integer part, count all digits
                return len(integer_part) + len(decimal_part)
            else:
                # If integer part is all zeros, count only non-zero digits and trailing zeros in decimal
                decimal_part = decimal_part.lstrip("0")
                return len(decimal_part) if decimal_part else 1
        else:
            # For whole numbers, trailing zeros are ambiguous
            # We'll assume they're significant if explicitly written
            s = s.lstrip("0")
            return len(s) if s else 1

    def _infer_sigfigs_from_float(self, x):
        # Default to a reasonable number for floats
        return 15

    def _get_decimal_places(self):
        """Calculate decimal places based on the original precision"""
        if self.value == 0:
            return 0

        # Find the position of the least significant digit
        order = math.floor(math.log10(abs(self.value)))
        least_sig_position = order - self.sigfigs + 1

        # Decimal places is the negative of the least significant position
        return max(0, -least_sig_position)

    # Arithmetic operations
    def __mul__(self, other):
        if not isinstance(other, SigFigNumber):
            other = SigFigNumber(other)
        val = self.value * other.value
        sig = min(self.sigfigs, other.sigfigs)
        return SigFigNumber(val, sig)

    def __truediv__(self, other):
        if not isinstance(other, SigFigNumber):
            other = SigFigNumber(other)
        val = self.value / other.value
        sig = min(self.sigfigs, other.sigfigs)
        return SigFigNumber(val, sig)

    def __add__(self, other):
        if not isinstance(other, SigFigNumber):
            other = SigFigNumber(other)
        val = self.value + other.value

        # Use decimal places rule for addition
        dec_self = self._get_decimal_places()
        dec_other = other._get_decimal_places()
        result_dec = min(dec_self, dec_other)

        # Round to the appropriate decimal place
        rounded_val = round(val, result_dec)

        # Calculate significant figures for the result
        if rounded_val == 0:
            result_sigfigs = 1
        else:
            # Count significant figures in the rounded result
            result_str = f"{rounded_val:.{result_dec}f}"
            result_sigfigs = self._count_sig_figs(result_str)

        return SigFigNumber(rounded_val, result_sigfigs)

    def __sub__(self, other):
        if not isinstance(other, SigFigNumber):
            other = SigFigNumber(other)
        val = self.value - other.value

        # Use decimal places rule for subtraction
        dec_self = self._get_decimal_places()
        dec_other = other._get_decimal_places()
        result_dec = min(dec_self, dec_other)

        # Round to the appropriate decimal place
        rounded_val = round(val, result_dec)

        # Calculate significant figures for the result
        if rounded_val == 0:
            result_sigfigs = 1
        else:
            result_str = f"{rounded_val:.{result_dec}f}"
            result_sigfigs = self._count_sig_figs(result_str)

        return SigFigNumber(rounded_val, result_sigfigs)

    # Support for right-hand operations
    def __rmul__(self, other):
        return self.__mul__(other)

    def __rtruediv__(self, other):
        other = SigFigNumber(other)
        return other.__truediv__(self)

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        other = SigFigNumber(other)
        return other.__sub__(self)

    def to_float(self):
        return self.value
