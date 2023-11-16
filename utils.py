import constants
from typing import Callable


def include_if(condition: bool, elements: list | Callable):
    if condition:
        if callable(elements):
            return elements()

        return elements
    else:
        return []


def get_color(color):
    return constants.COLORS.get(color) or color
