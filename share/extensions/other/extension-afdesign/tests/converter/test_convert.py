# Copyright (C) 2024 Jonathan Neuhauser <jonathan.neuhauser@outlook.com>
# SPDX-License-Identifier: GPL-2.0-or-later

from inkaf.afinput import AFInput
from inkex.tester import ComparisonMixin, TestCase
from inkex.tester.filters import CompareOrderIndependentStyle


class TestAFConverter(ComparisonMixin, TestCase):
    """Run-through tests of AFConverter"""

    effect_class = AFInput
    compare_file = [
        "./artboards_and_guides.afdesign",
        "./blend_modes.afdesign",
        "./blur.afdesign",
        "./image.afdesign",
        "./powerstroke.afdesign",
        "./rectangle_radius_tfm.afdesign",
        "./shapes.afdesign",
        "./text.afdesign",
        "./text_transform.afdesign",
        "./vector_crop.afdesign",
        "./vector_mask.afdesign",
        "./old_image_format.afdesign",
        "./crescent.afdesign",
        "./segment.afdesign",
        "./stars.afdesign",
        "./pie.afdesign",
        "./symbols_test.afdesign",
    ]
    comparisons = [tuple()]
    compare_filters = [CompareOrderIndependentStyle()]


class TestAdjustments(ComparisonMixin, TestCase):
    """"""

    effect_class = AFInput
    compare_file = ["./adjustments.afdesign"]
    comparisons = [tuple()]
    compare_filters = [CompareOrderIndependentStyle()]
    stderr_protect = False  # Allow
