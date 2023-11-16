from math import sqrt
import constants


def hexagon_dimensions(height, width):
    if height is not None and width is not None:
        return height, width
    elif height is not None:
        return height, height * 2 / sqrt(3)
    elif width is not None:
        return width * sqrt(3) / 2, width
    else:
        return constants.STANDARD_HEIGHT, constants.STANDARD_HEIGHT * 2 / sqrt(3)
