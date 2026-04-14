# SPDX-FileCopyrightText: 2024 Manpreet Singh <manpreet.singh.dev@proton.me>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from inkaf.svg.raster import AFImage, AFBitmap, AFImageTypes


def test_image_mime_type():
    image = AFImage(
        AFBitmap(0, 0, 0, None),
        file_path_abs=None,
        file_path_rel=None,
        file_size=0,
        file_type_enum=AFImageTypes.PNG,
        file_type_str=None,
    )

    assert image.media_type == "image/png"

    image.file_type_enum = None
    image.file_type_str = "PNG"
    assert image.media_type == "image/png"

    image.file_type_str = None
    image.file_path_rel = "test.png"
    assert image.media_type == "image/png"

    image.file_path_rel = None
    image.file_path_abs = "test.png"
    assert image.media_type == "image/png"

    image.file_path_abs = "test.jp2"
    assert image.media_type == "image/jp2"
