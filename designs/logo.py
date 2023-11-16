from generator import design
import svg
from paths import *


@design('logo_{}', ['white', 'black', 'transparent'])
def base_logo(background_color):
    return svg.SVG(
        viewBox=svg.ViewBoxSpec(
            0, 0, constants.STANDARD_HEIGHT, constants.STANDARD_HEIGHT),
        elements=[
            *include_if(background_color != 'transparent', lambda: [
                svg.Rect(
                        fill=get_color(background_color),
                        x=0,
                        y=0,
                        height=constants.STANDARD_HEIGHT,
                        width=constants.STANDARD_HEIGHT
                        ),
            ]),
            outlined_hexagon_path_elements(
                width=constants.STANDARD_HEIGHT - 20,
                with_logo=True,
                transform=[
                    svg.Translate(constants.STANDARD_HEIGHT /
                                  2, constants.STANDARD_HEIGHT / 2)
                ]
            ),
        ]
    )
