from math import sqrt
from typing import Optional
import svg
import constants
from calculations import hexagon_dimensions
from utils import *


def hexagon_path(height=constants.STANDARD_HEIGHT, width=None, ccw=False) -> list[svg.PathData]:
    height, width = hexagon_dimensions(height, width)

    s = height / sqrt(3)

    if ccw:
        s *= -1

    return [
        svg.MoveTo(-s, 0),
        svg.LineTo(-s/2, height/2),
        svg.LineTo(s/2, height/2),
        svg.LineTo(s, 0),
        svg.LineTo(s/2, -height/2),
        svg.LineTo(-s/2, -height/2),
        svg.ClosePath()
    ]


def outlined_hexagon_path_elements(
        height=None,
        width=None,
        top_left_color="orange",
        bottom_left_color="green",
        right_color="blue",
        all_colors=None,
        logo_color="white",
        with_logo=False,
        fill="gray_2",
        transform: Optional[list[svg.Transform]] = None,
):
    # Setup colors
    if all_colors is not None:
        right_color = top_left_color = bottom_left_color = all_colors

    # Compute correct height and width
    height, width = hexagon_dimensions(height, width)

    # Compute various dimensions
    normal_width = height * 2 / sqrt(3)
    outline_width = normal_width / 2 * constants.OUTLINE_WIDTH
    external_height = height / 2
    internal_height = external_height * (1 - outline_width * 2 / normal_width)
    external_width = width / 2
    internal_width = external_width - outline_width
    external_width_top = external_width - normal_width / 4
    internal_width_top = external_width_top - \
        sqrt(outline_width ** 2 - (external_height - internal_height) ** 2)

    # Create paths
    return [
        svg.Path(
            fill=get_color(top_left_color),
            transform=transform,
            d=[
                svg.M(-external_width, 0),
                svg.L(-external_width_top, -external_height),
                svg.L(external_width_top, -external_height),
                svg.L(internal_width_top, -internal_height),
                svg.L(-internal_width_top, -internal_height),
                svg.L(-internal_width, 0),
                svg.Z(),
            ],
        ),
        svg.Path(
            fill=get_color(bottom_left_color),
            transform=transform,
            d=[
                svg.M(-external_width, 0),
                svg.L(-external_width_top, external_height),
                svg.L(external_width_top, external_height),
                svg.L(internal_width_top, internal_height),
                svg.L(-internal_width_top, internal_height),
                svg.L(-internal_width, 0),
                svg.Z(),
            ],
        ),
        svg.Path(
            fill=get_color(right_color),
            transform=transform,
            d=[
                svg.M(external_width, 0),
                svg.L(external_width_top, external_height),
                svg.L(internal_width_top, internal_height),
                svg.L(internal_width, 0),
                svg.L(internal_width_top, -internal_height),
                svg.L(external_width_top, -external_height),
                svg.Z(),
            ],
        ),
        svg.Path(
            fill=get_color(fill),
            transform=transform,
            d=[
                svg.M(-internal_width, 0),
                svg.L(-internal_width_top, -internal_height),
                svg.L(internal_width_top, -internal_height),
                svg.L(internal_width, 0),
                svg.L(internal_width_top, internal_height),
                svg.L(-internal_width_top, internal_height),
                svg.Z(),
            ],
        ),
        include_if(with_logo, lambda: logo_elements(
            height=height * constants.LOGO_HEIGHT,
            offset_x=(normal_width - width) / 2,
            color=logo_color,
            transform=transform
        )),
    ]


def logo_elements(
        height=None,
        color="white",
        offset_x=0,
        transform: Optional[list[svg.Transform]] = None,
):
    # Compute correct height and width
    height, width = hexagon_dimensions(height, None)

    # Compute various dimensions
    side_length = height / sqrt(3)
    outline_width = width / 2 * constants.LOGO_WIDTH
    external_height = height / 2
    internal_height = external_height * (1 - outline_width * 2 / width)
    external_width = width / 2
    internal_width = external_width - outline_width
    external_width_top = external_width - width / 4
    internal_width_top = external_width_top - \
        sqrt(outline_width ** 2 - (external_height - internal_height) ** 2)
    logo_end_height = external_height - \
        constants.LOGO_ENDS_LENGTH * side_length * sqrt(3) / 2
    external_logo_end_width = external_width_top + \
        constants.LOGO_ENDS_LENGTH * side_length / 2
    internal_logo_end_width = external_logo_end_width - outline_width

    # Create paths
    return [
        svg.Path(
            fill=get_color(color),
            transform=transform,
            d=[
                # Top line of top section
                svg.M(offset_x + -external_width_top, -external_height),
                svg.L(offset_x + external_width_top, -external_height),

                # Right side of middle section
                svg.L(offset_x + external_width_top + outline_width / \
                      6 * sqrt(3), -external_height + outline_width / 2),
                svg.L(offset_x + -internal_width_top + \
                      outline_width / 2, internal_height),

                # Top line of bottom section
                svg.L(offset_x + internal_width_top, internal_height),

                # Bottom end
                svg.L(offset_x + internal_logo_end_width, logo_end_height),
                svg.L(offset_x + external_logo_end_width, logo_end_height),

                # Bottom line of bottom section
                svg.L(offset_x + external_width_top, external_height),
                svg.L(offset_x + -external_width_top, external_height),

                # Left side of middle section
                svg.L(offset_x - external_width_top - outline_width / \
                      6 * sqrt(3), external_height - outline_width / 2),
                svg.L(offset_x + internal_width_top - \
                      outline_width / 2, -internal_height),

                # Bottom line of top section
                svg.L(offset_x + -internal_width_top, -internal_height),

                # Top end
                svg.L(offset_x + -internal_logo_end_width, -logo_end_height),
                svg.L(offset_x + -external_logo_end_width, -logo_end_height),
                svg.Z(),
            ],
        ),
    ]
