# coding=utf-8
#
# Copyright (C) 2007 Martin Owens
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
Python barcode renderer for UPCA barcodes. Designed for use with Inkscape.
"""

from .BaseEan import EanBarcode


class Upca(EanBarcode):
    """Provides a renderer for EAN12 aka UPC-A Barcodes"""

    name = "upca"
    font_size = 10
    lengths = [11]
    checks = [12]

    def _encode(self, num, guide=False):
        """Encode for a UPC-A Barcode"""
        self.text = EanBarcode.space(num[0:1], 3, num[1:6], 4, num[6:11], 3, num[11:])
        return self.enclose(
            EanBarcode.encode_left(num[0:6]),
            EanBarcode.encode_right(num[6:12]),
        )
