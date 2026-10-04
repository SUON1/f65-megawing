"""Inspect pinned Xemu PNG pixels without modifying an image or tested carrier."""
import binascii
from pathlib import Path
import struct
import zlib

ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / ('docs/evidence/r0f/group1/2026-10-03-audio-readback/'
                    'focused/export-failure-01/screen.png')


def text_pixels(data):
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('PNG signature')
    position, packed, palette, geometry = 8, bytearray(), None, None
    ended = False
    while position < len(data):
        size = int.from_bytes(data[position:position + 4], 'big')
        kind = data[position + 4:position + 8]
        payload = data[position + 8:position + 8 + size]
        stop = position + size + 12
        if (stop > len(data) or binascii.crc32(kind + payload) & 0xffffffff
                != int.from_bytes(data[stop - 4:stop], 'big')):
            raise ValueError('PNG chunk integrity')
        if kind == b'IHDR':
            geometry = struct.unpack('>IIBBBBB', payload)
        elif kind == b'PLTE':
            palette = [payload[i:i + 3] for i in range(0, len(payload), 3)]
        elif kind == b'IDAT':
            packed.extend(payload)
        elif kind == b'IEND':
            ended = True
        position = stop
    if not ended or geometry is None or palette is None:
        raise ValueError('PNG incomplete')
    width, height, depth, color, compression, filtering, interlace = geometry
    if (width != 800 or not 400 <= height <= 700
            or (depth, color, compression, filtering, interlace) != (2, 3, 0, 0, 0)
            or b'\xf0\xf0\xf0' not in palette):
        raise ValueError('Pinned Xemu PNG format/palette')
    white = palette.index(b'\xf0\xf0\xf0')
    stride = width // 4
    raw = zlib.decompress(packed)
    if len(raw) != (stride + 1) * height:
        raise ValueError('PNG scanline length')
    points = set()
    for y in range(height):
        first = y * (stride + 1)
        if raw[first] != 0:
            raise ValueError('Unexpected pinned Xemu PNG filter')
        row = raw[first + 1:first + 1 + stride]
        for x in range(width):
            if (row[x // 4] >> (6 - 2 * (x % 4))) & 3 == white:
                points.add((x, y))
    if not points:
        raise ValueError('Blank operator screen')
    left = min(x for x, _ in points)
    top = min(y for _, y in points)
    return frozenset((x - left, y - top) for x, y in points)


def validate_collision_screen(path):
    # The retained screenshot supplies the complete readable S5/E03/F00
    # glyph pattern. Normalize position only for PAL/NTSC top-border changes;
    # never normalize glyphs, text, missing pixels, colors or scale.
    observed = text_pixels(Path(path).read_bytes())
    expected = text_pixels(REFERENCE.read_bytes())
    if observed != expected:
        raise ValueError('Collision screen glyphs differ from retained reference')
    return {'result': 'PASS_REFERENCE_BITMAP', 'reference': str(REFERENCE),
            'whiteTextPixels': len(observed), 'positionOnlyNormalization': True}
