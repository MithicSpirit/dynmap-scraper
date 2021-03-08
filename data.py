"""
Obtains data from a cache or from the dynmap.
"""

from io import BytesIO
import requests
from os import mkdir
from time import sleep
from PIL import Image
from typing import Optional


def _get(*args, wrapper_depth: int = 0, **kwargs):
    try:
        return requests.get(*args, **kwargs, timeout=30)
    except requests.exceptions.RequestException as err:
        if wrapper_depth > 3:
            raise err
        print("Connection refused, trying again in 60 seconds…")
        sleep(60)
        print("Trying again now")
        return _get(*args, wrapper_depth=wrapper_depth + 1, **kwargs)


def worldborder(
    baselink: str, world: str
) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Scrapes the dynmap data to obtain the world border radius.
    """
    data = _get(f"{baselink}tiles/_markers_/marker_{world}.json").json()
    border_data = data["sets"]["markers"]["areas"][f"_worldborder_{world}"]
    X = border_data["x"]
    Z = border_data["z"]
    rangeX = min(X), max(X)
    rangeZ = min(Z), max(Z)

    return rangeX, rangeZ


def getimage(
    templates: tuple[str, Optional[str]], xpos: int, zpos: int, zoom: int
) -> Image:
    """
    Obtains the image for a tile at a specified position, adjusted for zoom and
    z reflection.
    """
    xpos *= 2 ** zoom
    zpos *= -(2 ** zoom)
    link = templates[0].format(x=xpos, z=zpos)
    cache = templates[1]

    if cache is not None:
        cache = templates[1].format(x=xpos, z=zpos)
        try:
            return Image.open(cache)
        except FileNotFoundError:
            tile_data = _get(link.format(x=xpos, z=zpos))
            image = Image.open(BytesIO(tile_data.content))
            image.save(cache)
            return image

    tile_data = _get(link.format(x=xpos, z=zpos))
    return Image.open(BytesIO(tile_data.content))


def templating(
    baselink: str, cachefolder: Optional[str], world: str, zoom: int
) -> tuple[str, Optional[str]]:
    """
    Creates a link and a cache template for `getimage` from the values in the
    arguments. If the `cachefolder` directory does not exist, it is created.
    """
    zoomstr = "z" * zoom + "_" if zoom else ""
    link = f"{baselink}tiles/{world}/flat/0_0/{zoomstr}" + "{x}_{z}.png"

    cache = f"{cachefolder}/{world}_{zoomstr}" + "{x}_{z}.png"
    try:
        if cachefolder:
            mkdir(cachefolder)
    except FileExistsError:
        print(f"Cache folder “{cachefolder}” already exists. Continuing.")
    except OSError:
        print(
            "Unable to create cache folder “{cachefolder}”. Continuing without a cache."
        )
        cache = None
    else:
        print(f"Cache folder “{cachefolder}” was created.")

    return (link, cache)
