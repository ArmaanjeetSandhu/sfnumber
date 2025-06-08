import math
import re
import warnings


class SigFigNumber:
    def __init__(self, value, sigfigs=None):
        if isinstance(value, str):
            self.original_str = value.strip()
            self.value = float(value)
            self.sigfigs = (
                self._count_sig_figs(self.original_str) if sigfigs is None else sigfigs
            )
        elif isinstance(value, (int, float)):
            if sigfigs is None:
                raise ValueError(
                    "When initializing with a number, sigfigs must be provided."
                )
            self.value = float(value)
            self.sigfigs = sigfigs
            self.original_str = self._format_to_sig_figs(self.value, self.sigfigs)
        else:
            raise TypeError("Unsupported type for SigFigNumber.")

    def __repr__(self):
        return f"{self._rounded_str()} (±{self.sigfigs} sf)"

    def _rounded_str(self):
        return self._format_to_sig_figs(self.value, self.sigfigs)

    def _format_to_sig_figs(self, x, sigfigs):
        if x == 0:
            # Represent zero with appropriate decimal places if originally decimal zeros
            if self.original_str and "." in self.original_str:
                dec_len = len(self.original_str.split(".")[-1])
                return f"0.{'0' * (dec_len)}"
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
            int_nonzero = integer_part.lstrip("0")

            if int_nonzero:
                # If there's a non-zero integer part, count all digits (including decimals)
                return len(int_nonzero) + len(decimal_part)
            else:
                # If integer part is all zeros, strip leading zeros in decimal
                dec_strip_lead = decimal_part.lstrip("0")
                if dec_strip_lead:
                    # Count all digits after leading zeros
                    return len(dec_strip_lead)
                else:
                    # All zeros in decimal (e.g., "0.000"), count all decimal places
                    return len(decimal_part)
        else:
            # For whole numbers, trailing zeros are ambiguous
            # We assume trailing zeros are NOT significant unless a decimal point or exponent was present
            stripped = s.lstrip("0")  # remove leading zeros
            if not stripped:
                # The number is 0 or 00... ambiguous, treat as 1 sig fig
                return 1
            # Count digits before trailing zeros
            sig_digits = len(stripped.rstrip("0"))
            if sig_digits == 0:
                # E.g., "0000" -> treat as 1 sf
                return 1
            # If trailing zeros exist, warn the user
            if stripped.endswith("0"):
                warnings.warn(
                    f"Ambiguous sig fig count for '{s}'; assuming trailing zeros are not significant."
                )
            return sig_digits

    def _get_decimal_places(self):
        """Calculate decimal places based on the stored sig figs and value"""
        if self.value == 0:
            if (
                hasattr(self, "original_str")
                and self.original_str
                and "." in self.original_str
            ):
                return len(self.original_str.split(".")[-1])
            return 0

        order = math.floor(math.log10(abs(self.value)))
        least_sig_position = order - self.sigfigs + 1
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

        dec_self = self._get_decimal_places()
        dec_other = other._get_decimal_places()
        result_dec = min(dec_self, dec_other)

        rounded_val = round(val, result_dec)

        if rounded_val == 0:
            result_sigfigs = 1
        else:
            result_str = f"{rounded_val:.{result_dec}f}"
            result_sigfigs = self._count_sig_figs(result_str)

        return SigFigNumber(rounded_val, result_sigfigs)

    def __sub__(self, other):
        if not isinstance(other, SigFigNumber):
            other = SigFigNumber(other)
        val = self.value - other.value

        dec_self = self._get_decimal_places()
        dec_other = other._get_decimal_places()
        result_dec = min(dec_self, dec_other)

        rounded_val = round(val, result_dec)

        if rounded_val == 0:
            result_sigfigs = 1
        else:
            result_str = f"{rounded_val:.{result_dec}f}"
            result_sigfigs = self._count_sig_figs(result_str)

        return SigFigNumber(rounded_val, result_sigfigs)

    # Unary operations
    def __neg__(self):
        return SigFigNumber(-self.value, self.sigfigs)

    def __abs__(self):
        return SigFigNumber(abs(self.value), self.sigfigs)

    # Comparison operators
    def __eq__(self, other):
        if not isinstance(other, SigFigNumber):
            try:
                other = SigFigNumber(other)
            except:
                return False
        return math.isclose(self.value, other.value)

    def __lt__(self, other):
        if not isinstance(other, SigFigNumber):
            other = SigFigNumber(other)
        return self.value < other.value

    def __le__(self, other):
        if not isinstance(other, SigFigNumber):
            other = SigFigNumber(other)
        return self.value <= other.value

    def __gt__(self, other):
        if not isinstance(other, SigFigNumber):
            other = SigFigNumber(other)
        return self.value > other.value

    def __ge__(self, other):
        if not isinstance(other, SigFigNumber):
            other = SigFigNumber(other)
        return self.value >= other.value

    # Right-hand operations
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

    # Logarithmic and exponential functions
    def log10(self):
        if self.value <= 0:
            raise ValueError("Logarithm undefined for non-positive values.")
        raw = math.log10(self.value)
        # Decimal places = number of sig figs in input
        dec_places = self.sigfigs
        rounded = round(raw, dec_places)
        # Return as a float string with correct decimal places
        return f"{rounded:.{dec_places}f}"

    def ln(self):
        if self.value <= 0:
            raise ValueError("Logarithm undefined for non-positive values.")
        raw = math.log(self.value)
        dec_places = self.sigfigs
        rounded = round(raw, dec_places)
        return f"{rounded:.{dec_places}f}"

    def exp(self):
        raw = math.exp(self.value)
        # Sig figs in result = decimal places of exponent
        dec_places = self._get_decimal_places()
        # Convert dec_places to sig figs for the result
        if raw == 0:
            return SigFigNumber(0, 1)
        result_sigfigs = max(1, dec_places)
        return SigFigNumber(raw, result_sigfigs)

    def sqrt(self):
        if self.value < 0:
            raise ValueError("Square root undefined for negative values.")
        raw = math.sqrt(self.value)
        sig = self.sigfigs
        return SigFigNumber(raw, sig)
