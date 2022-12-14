# coding=utf-8
#
# Copyright (C) 2010 Martin Owens
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110, USA.
#
"""
Some basic common code shared between EAN and UCP generators.
"""

from .Base import Barcode, TEXT_POS_TOP
from inkex.localization import inkex_gettext as _

try:
    from typing import Optional, List, Dict
except ImportError:
    pass

MAPPING = [
    # Left side of barcode Family '0'
    [
        "0001101",
        "0011001",
        "0010011",
        "0111101",
        "0100011",
        "0110001",
        "0101111",
        "0111011",
        "0110111",
        "0001011",
    ],
    # Left side of barcode Family '1' and flipped to right side.
    [
        "0100111",
        "0110011",
        "0011011",
        "0100001",
        "0011101",
        "0111001",
        "0000101",
        "0010001",
        "0001001",
        "0010111",
    ],
]
# This chooses which of the two encodings above to use.
FAMILIES = (
    "000000",
    "001011",
    "001101",
    "001110",
    "010011",
    "011001",
    "011100",
    "010101",
    "010110",
    "011010",
)


class EanBarcode(Barcode):
    """Simple base class for all EAN type barcodes"""

    lengths = None  # type: Optional[List[int]]
    length = None  # type: Optional[int]
    checks = []  # type: List[int]
    extras = {}  # type: Dict[int, str]
    magic = 10
    guard_bar = "202"
    center_bar = "02020"

    @staticmethod
    def intarray(number):
        """Convert a string of digits into an array of ints"""
        return [int(i) for i in number]

    @staticmethod
    def encode_interleaved(family, number, fams=FAMILIES):
        """Encode any side of the barcode, interleaved"""
        result = []
        encset = EanBarcode.intarray(fams[family])
        for i, _ in enumerate(number):
            thismap = MAPPING[encset[i]]
            result.append(thismap[number[i]])
        return result

    @staticmethod
    def encode_right(number):
        """Encode the right side of the barcode, non-interleaved"""
        result = []
        for num in number:
            # The right side is always the reverse of the left's family '1'
            result.append(MAPPING[1][num][::-1])
        return result

    @staticmethod
    def encode_left(number):
        """Encode the left side of the barcode, non-interleaved"""
        result = []
        for num in number:
            result.append(MAPPING[0][num])
        return result

    @staticmethod
    def space(*spacing):
        """Space out an array of numbers"""
        result = ""
        for space in spacing:
            if isinstance(space, list):
                for i in space:
                    result += str(i)
            elif isinstance(space, int):
                result += " " * space
        return result

    def get_lengths(self):
        """Return a list of acceptable lengths"""
        if self.length:
            return [self.length]
        return self.lengths[:]

    def encode(self, text):
        """Encode any EAN barcode"""
        code = text.replace(" ", "").strip()
        guide = code.endswith(">")
        code = code.strip(">")

        if not code.isdigit():
            return self.error(code, _("Not a Number, must be digits 0-9 only"))
        lengths = self.get_lengths() + self.checks

        # Allow extra barcodes after the first one
        if len(code) not in lengths:
            for extra in self.extras:
                sep = len(code) - extra
                if sep in lengths:
                    # Generate a barcode along side this one.
                    self.add_extra_barcode(
                        self.extras[extra],
                        text=code[sep:],
                        x=self.pos_x + 400 * self.scale,
                        text_pos=TEXT_POS_TOP,
                    )
                    code = code[:sep]

        if len(code) not in lengths:
            return self.error(
                code,
                _("Wrong size {:d}, must be {} digits").format(
                    len(code), ", ".join([str(length) for length in lengths])
                ),
            )

        if self.checks:
            if len(code) not in self.checks:
                code = self.append_checksum(code)
            elif not self.verify_checksum(code):
                return self.error(code, _("Checksum failed, omit for new sum"))
        return self._encode(EanBarcode.intarray(code), guide=guide)

    def _encode(self, num, guide=False):
        """
        Write your EAN encoding function, it's passed in an array of int and
        it should return a string on 1 and 0 for black and white parts
        """
        raise NotImplementedError("_encode should be provided by parent EAN")

    def enclose(self, left, right=()):
        """Standard Enclosure"""
        parts = [self.guard_bar] + left
        parts.append(self.center_bar)
        parts += list(right) + [self.guard_bar]
        return "".join(parts)

    def get_checksum(self, num):
        """Generate a UPCA/EAN13/EAN8 Checksum"""
        # Left to right,checksum based on first digits.
        total = sum([int(n) * (3, 1)[x % 2] for x, n in enumerate(num[::-1])])
        # Modulous result to a single digit checksum
        checksum = self.magic - (total % self.magic)
        if checksum < 0 or checksum >= self.magic:
            return "0"
        return str(checksum)

    def append_checksum(self, number):
        """Apply the checksum to a short number"""
        return number + self.get_checksum(number)

    def verify_checksum(self, number):
        """Verify any checksum"""
        return self.get_checksum(number[:-1]) == number[-1]
