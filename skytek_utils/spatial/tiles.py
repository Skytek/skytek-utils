import math
from typing import Tuple


def deg2tile(lon_deg: float, lat_deg: float, zoom: int) -> Tuple[int, int, int]:
    """Converts lon/lat to a tile xyz coords"""
    lat_rad = math.radians(lat_deg)
    n = 2.0**zoom  # pylint: disable=invalid-name
    tile_x = int((lon_deg + 180.0) / 360.0 * n)
    tile_y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return tile_x, tile_y, zoom


def tile2deg(tile_x: int, tile_y: int, zoom: int) -> Tuple[float, float]:
    """This returns the NW-corner of the square"""
    n = 2.0**zoom  # pylint: disable=invalid-name
    lon_deg = tile_x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * tile_y / n)))
    lat_deg = math.degrees(lat_rad)
    return lon_deg, lat_deg


def deg2tile_with_offset(
    lon_deg: float, lat_deg: float, zoom: int
) -> Tuple[Tuple[int, int, int], Tuple[int, int]]:
    """Converts lon/lat to a tile xyz coords and pixel xy coords on that tile"""
    tile_x, tile_y, _ = deg2tile(lon_deg, lat_deg, zoom)
    tile_nw_lon, tile_nw_lat = tile2deg(tile_x, tile_y, zoom)
    tile_se_lon, tile_se_lat = tile2deg(tile_x + 1, tile_y + 1, zoom)

    tile_width = tile_height = 256

    offset_x = int(tile_width * (lon_deg - tile_nw_lon) / (tile_se_lon - tile_nw_lon))
    offset_y = int(tile_height * (lat_deg - tile_nw_lat) / (tile_se_lat - tile_nw_lat))

    return (tile_x, tile_y, zoom), (offset_x, offset_y)


def tile_with_offset2deg(
    tile_x: int, tile_y: int, zoom: int, offset_x: int, offset_y
) -> Tuple[float, float]:
    """Returns lon/lat coordinates of a pixel on a tile"""
    tile_width = tile_height = 256

    tile_nw_lon, tile_nw_lat = tile2deg(tile_x, tile_y, zoom)
    tile_se_lon, tile_se_lat = tile2deg(tile_x + 1, tile_y + 1, zoom)

    offset_lon = (tile_se_lon - tile_nw_lon) * (offset_x / tile_width)
    offset_lat = (tile_se_lat - tile_nw_lat) * (offset_y / tile_height)

    return tile_nw_lon + offset_lon, tile_nw_lat + offset_lat
