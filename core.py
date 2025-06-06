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
        exponent = math.floor(math.log10(abs(x)))
        decimals = sigfigs - exponent - 1
        return f"{round(x, decimals):.{max(0, decimals)}f}"

    def _count_sig_figs(self, s):
        s = s.strip()
        if "e" in s.lower():
            s = s.lower().split("e")[0]

        # Remove signs
        s = re.sub(r"[+-]", "", s)

        # Handle numbers like ".0340"
        if "." in s:
            s = s.strip("0")  # remove both leading and trailing
            digits = re.sub(r"\.", "", s)
            return len(digits)
        else:
            s = s.lstrip("0")
            return len(s)

    def _infer_sigfigs_from_float(self, x):
        # Can't really tell from float alone — default to 15
        return 15

    # Arithmetic
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
        # Use decimal places rule
        dec_self = self._decimal_places()
        dec_other = other._decimal_places()
        result_dec = min(dec_self, dec_other)
        rounded_val = round(val, result_dec)
        return SigFigNumber(
            rounded_val, self._sig_figs_from_decimals(rounded_val, result_dec)
        )

    def __sub__(self, other):
        if not isinstance(other, SigFigNumber):
            other = SigFigNumber(other)
        val = self.value - other.value
        dec_self = self._decimal_places()
        dec_other = other._decimal_places()
        result_dec = min(dec_self, dec_other)
        rounded_val = round(val, result_dec)
        return SigFigNumber(
            rounded_val, self._sig_figs_from_decimals(rounded_val, result_dec)
        )

    def _decimal_places(self):
        # Number of decimal places in original value
        if "." in str(self._rounded_str()):
            return len(str(self._rounded_str()).split(".")[-1])
        return 0

    def _sig_figs_from_decimals(self, x, decimal_places):
        if x == 0:
            return 1
        return max(1, len(str(x).replace(".", "").lstrip("0")))

    def to_float(self):
        return self.value
