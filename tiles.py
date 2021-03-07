"""
For dealing with dynmap tiles.
"""

from math import floor, ceil

from consts import Z_OFFSET, TILE_BASE_SIZE


def get_tilesize(zoom):
    """
    Converts the zoom level to the new tilesize (in blocks).
    """
    return TILE_BASE_SIZE * (2 ** zoom)


def blocks_to_tiles(
    minX: int, maxX: int, minZ: int, maxZ: int, tilesize: int
) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Returns a tuple of tuples specifying the x and z ranges for the necessary
    tiles to be obtained from given ranges of blocks (and the tilesize).
    """
    min_tileX = floor(minX / tilesize)
    max_tileX = ceil(maxX / tilesize)

    minZ += Z_OFFSET
    min_tileZ = floor(minZ / tilesize)
    maxZ += Z_OFFSET
    max_tileZ = ceil(maxZ / tilesize)

    return ((min_tileX, max_tileX), (min_tileZ, max_tileZ))


def tiles_to_blocks(
    minX: int, maxX: int, minZ: int, maxZ: int, tilesize: int
) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Reverses the effect of `blocks_to_tiles`, but keeps the extra padding.
    """
    min_blockX = minX * tilesize
    max_blockX = maxX * tilesize

    min_blockZ = minZ * tilesize
    min_blockZ -= Z_OFFSET
    max_blockZ = maxZ * tilesize
    max_blockZ -= Z_OFFSET

    return ((min_blockX, max_blockX), (min_blockZ, max_blockZ))
