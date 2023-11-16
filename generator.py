import svg
from typing import TypeAlias
import os
import importlib
import cairosvg
import constants

ResultSVG: TypeAlias = tuple[str, svg.SVG]


class DesignResults:
    designs: list[ResultSVG]

    def __init__(self, designs: list[ResultSVG]):
        self.designs = designs


def design(name: str, arguments: list = []):
    """
    Decorator to indicate that this is a function that generates an SVG.
    Use the `arguments` parameter to run this function multiple times with
    different arguments.
    """
    def decorator(func):
        nonlocal name
        nonlocal arguments

        if len(arguments) == 0:
            arguments = [()]

        arguments = [
            args if args is list or args is tuple else (args,) for args in arguments
        ]

        results = []

        for args in arguments:
            results.append((name.format(*args), func(*args)))

        return DesignResults(results)

    return decorator


if __name__ == '__main__':
    # Go through each of the design files and look for methods annotated with @design
    root_dir = os.path.join(os.getcwd(), 'designs')

    groups: dict[str, list[ResultSVG]] = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".py") and os.path.join(root_dir, filename) != __file__:
                filename = filename.removesuffix(".py")
                module = importlib.import_module(f'designs.{filename}')
                for k, v in module.__dict__.items():
                    if type(v).__name__ == 'DesignResults':
                        for name, result_svg in v.designs:
                            output_filename = os.path.join(
                                os.getcwd(), 'output', filename, f'{name}.svg'
                            )
                            output_filename_png = os.path.join(
                                os.getcwd(),
                                'output',
                                filename,
                                f'{name}@{{}}.png'
                            )
                            os.makedirs(
                                os.path.dirname(output_filename),
                                exist_ok=True
                            )

                            # Write SVG
                            with open(output_filename, 'w') as f:
                                print(
                                    f'[{filename}] [{name}] [SVG]          -> {output_filename}'
                                )
                                f.write(str(result_svg))

                            # Write PNGs in various sizes
                            for height in constants.PNG_HEIGHTS:
                                with open(output_filename, 'r') as f:
                                    png_filename = output_filename_png.format(
                                        height
                                    )
                                    print(
                                        ' ' * len(f'[{filename}] [{name}] ') +
                                        f'[PNG @ {height}px] {" " * (4-len(str(height)))}-> {png_filename}'
                                    )
                                    cairosvg.svg2png(
                                        file_obj=f,
                                        output_height=height,
                                        write_to=png_filename
                                    )
