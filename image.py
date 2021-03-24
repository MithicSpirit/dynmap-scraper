from math import floor, ceil
from PIL import Image

import tiles
from consts import TILE_BASE_SIZE_PX, BLOCK_BASE_SIZE_PX


def init(rangeX: tuple[int, int], rangeZ: tuple[int, int]) -> Image:
    """
    Creates an image of the appropriate size.
    """
    size_pxX = (rangeX[1] - rangeX[0]) * TILE_BASE_SIZE_PX
    size_pxZ = (rangeZ[1] - rangeZ[0]) * TILE_BASE_SIZE_PX
    image = Image.new("RGB", (size_pxX, size_pxZ))
    Image.MAX_IMAGE_PIXELS = max(size_pxX * size_pxZ, Image.MAX_IMAGE_PIXELS)
    return image


def append(original: Image, newdata: Image, posx: int, posz: int) -> None:
    """
    "Appends" a new tile to the original image in the correct position.
    """
    pos = (posx * TILE_BASE_SIZE_PX, posz * TILE_BASE_SIZE_PX)
    original.paste(newdata, pos)


def trim(
    full_map: Image,
    zoom: int,
    size: tuple[tuple[int, int], tuple[int, int]],
    size_tiles: tuple[tuple[int, int], tuple[int, int]],
) -> Image:
    """
    Trims the full_map image to not include anything after the desired borders.
    """

    tilesize = tiles.get_tilesize(zoom)
    curr = tiles.tiles_to_blocks(*size_tiles[0], *size_tiles[1], tilesize)

    offset_blocksX = size[0][0] - curr[0][0]
    end_blocksX = size[0][1] - curr[0][0]
    offset_blocksZ = size[1][0] - curr[1][0]
    end_blocksZ = size[1][1] - curr[1][0]

    BLOCK_SIZE = BLOCK_BASE_SIZE_PX / (2 ** zoom)

    offsetX = floor(offset_blocksX * BLOCK_SIZE)
    endX = ceil(end_blocksX * BLOCK_SIZE)
    offsetZ = floor(offset_blocksZ * BLOCK_SIZE)
    endZ = ceil(end_blocksZ * BLOCK_SIZE)

    return full_map.crop((offsetX, offsetZ, endX, endZ))


"""
def save(image: Image, output: Optional[str]):
    filetype = "png"
    if output:
        ind = output.rfind('.')
        if ind != -1 and ind != len(output) - 1:
            filetype = filetype[ind + 1:]
    with BytesIO() as buffer_:
        image.save(buffer_, format=filetype)
        if output:
            with open(output, "wb") as outfile:
                outfile.write(buffer_.getbuffer())
        else:
            """
