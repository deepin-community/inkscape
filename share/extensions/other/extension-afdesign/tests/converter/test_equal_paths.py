# SPDX-FileCopyrightText: 2024 Jonathan Neuhauser <jonathan.neuhauser@outlook.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import inkex
import pytest
from inkaf.parser.extract import AFExtractor
from inkaf.svg.convert import AFConverter


def split_arcs(path: inkex.Path):
    p2 = inkex.Path()
    for cmd in path.to_absolute().proxy_iterator():
        if cmd.letter == "A":
            split = cmd.split(0.5)
            p2.append(split[0].command)
            p2.append(split[1].command)

        else:
            p2.append(cmd.command)
    return p2


def prepare(element: inkex.ShapeElement) -> inkex.Path:
    if isinstance(element, inkex.Polygon):
        element = inkex.PathElement.new(element.get_path().transform(element.transform))

    element.apply_transform()
    element.apply_transform()

    return split_arcs(element.path.to_absolute())


@pytest.mark.parametrize(
    "file",
    [
        "./stars_curved_sides.afdesign",
        "./heart.afdesign",
        "./polygons.afdesign",
        "./tear.afdesign",
        "./clouds.afdesign",
        "./fancystars.afdesign",
    ],
)
def test_stars_curved(file):
    with open("tests/converter/data/" + file, "rb") as stream:
        converter = AFConverter()
        converter.convert(AFExtractor(stream))
        output = converter.doc.getroot()

    # There are two groups in the resulting SVG. One contains the stars as
    # paths (converted in Designer), one as stars.
    # Both should have the same paths in the end.
    groups = [g for g in output if isinstance(g, inkex.Group)]

    for pe1, pe2 in zip(groups[0], groups[1]):
        p1 = prepare(pe1)
        p2 = prepare(pe2)

        for cm1, cm2 in zip(p1.proxy_iterator(), p2.proxy_iterator()):
            if cm1.letter == "A" or cm2.letter == "A":
                continue
            if cm1.letter != cm2.letter:
                # Z and L
                assert cm1.end_point.is_close(cm2.end_point, rtol=1e-4)
                assert cm1.letter in "ZL", (p1, p2)
                assert cm2.letter in "ZL"
            else:
                for pt1, pt2 in zip(cm1.control_points, cm2.control_points):
                    assert pt1.is_close(pt2, rtol=1e-4)

        assert p1.bounding_box().center.is_close(p2.bounding_box().center, rtol=1e-3)

    assert len(groups[1]) > 3
