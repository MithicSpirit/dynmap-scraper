#!/usr/bin/env python3.9
"""Usage: cli.py [options] <link> <world>

Options:
  -h --help                      Display this help message.
  -c [folder], --cache=[folder]  Optionally set a cache folder.
                                 [default: cache]
  -C, --no-cache                 Disables cache (overrides --cache).
  -o <file>, --output=<file>     Specifies which file to output the image to
                                 [default: dynmap.png]
  --size=[x1,x2,z1,z2]           A comma-separated list of the coordinates of
                                 the region from which to download the map. Set
                                 to `worldborder' to attempt to utilize the
                                 world border size instead.
                                 [default: worldborder]
  -z <level>, --zoom=<level>     Zoom level to download the map at, 0 is
                                 highest resolution (zoomed in) and 5 is
                                 minimum resolution (zoomed out). [default: 0]
"""

import sys
from typing import NoReturn
from docopt import docopt

import main as primary


def main():
    """
    Takes care of arguments and passes results on to `main.py`.
    """
    arguments: dict = docopt(__doc__)
    print(arguments)
    fixargs(arguments)
    print(arguments)
    primary.run(
        arguments["<link>"],
        arguments["<world>"],
        arguments["--output"],
        arguments["--cache"],
        arguments["--size"],
        arguments["--zoom"],
    )


def fixargs(arguments: dict):
    """
    Checks and patches (in-place) arguments to make sure they are good.
    """
    try:
        zoom = arguments["--zoom"] = int(arguments["--zoom"])
        if zoom < 0 or zoom > 5:
            raise ValueError(zoom)
    except ValueError:
        error("Invalid zoom level.")
    size = arguments["--size"]
    try:
        if size == "worldborder":
            arguments["--size"] = None
        else:
            size_list = size.split(",")
            if len(size_list) != 4:
                raise ValueError(size)
            size_list = tuple(int(pos) for pos in size_list)
            if size_list[0] > size_list[1] or size_list[2] > size_list[3]:
                raise ValueError(size)
            arguments["--size"] = (size_list[:2], size_list[2:])
    except ValueError:
        error("Invalid size value.")

    if arguments["--no-cache"]:
        arguments["--cache"] = None
    else:
        arguments["--cache"] = arguments["--cache"].rstrip("/")

    del arguments["--no-cache"], arguments["--help"]


def error(message, code=1) -> NoReturn:
    """
    Prints `message` then exits with `code`.
    """
    if message:
        print(message)
    sys.exit(code)


if __name__ == "__main__":
    main()
