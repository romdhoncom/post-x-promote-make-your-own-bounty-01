#!/usr/bin/env python3
"""Draw photo.png for the make-your-own-bounty X post.

Pure Python standard library only: an own raster canvas, an own 5x7
bitmap font, and an own PNG encoder. No PIL, no external files, no
network. The picture is original: a dusk sky, a big headline, a wooden
bounty board with three pinned bounty cards, and gold coins. No logo of
any kind is drawn; the name make.fun appears only as plain text.

Run: python3 make_photo.py  ->  writes photo.png (1200x675) next to it.
"""

import random
import struct
import zlib

W, H = 1200, 675

# ---------------------------------------------------------------- canvas
# RGB canvas, one byte per channel.
canvas = bytearray(W * H * 3)


def put(x, y, rgb):
    """Set one pixel, silently ignoring out-of-bounds coordinates."""
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        canvas[i] = rgb[0]
        canvas[i + 1] = rgb[1]
        canvas[i + 2] = rgb[2]


def rect(x0, y0, x1, y1, rgb):
    """Fill an axis-aligned rectangle, clipped to the canvas."""
    x0 = max(0, x0)
    y0 = max(0, y0)
    x1 = min(W, x1)
    y1 = min(H, y1)
    for y in range(y0, y1):
        base = (y * W + x0) * 3
        for x in range(x0, x1):
            i = base + (x - x0) * 3
            canvas[i] = rgb[0]
            canvas[i + 1] = rgb[1]
            canvas[i + 2] = rgb[2]


def circle(cx, cy, r, rgb):
    """Fill a disc with the midpoint scanline method."""
    for dy in range(-r, r + 1):
        dx = int((r * r - dy * dy) ** 0.5)
        for x in range(cx - dx, cx + dx + 1):
            put(x, cy + dy, rgb)


def disc_outline(cx, cy, r, rgb):
    """Draw a 2px ring around a disc."""
    for dy in range(-r - 1, r + 2):
        for dx in range(-r - 1, r + 2):
            d2 = dx * dx + dy * dy
            if (r - 1) ** 2 <= d2 <= (r + 1) ** 2:
                put(cx + dx, cy + dy, rgb)


# ------------------------------------------------------------------- font
# 5x7 bitmap font, one row per string, '1' is ink. Only the glyphs the
# picture needs: capitals, digits, a few lowercase letters and marks.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    "a": ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    "f": ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    "k": ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    "m": ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    "n": ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    "u": ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
}


def text_width(s, scale):
    """Pixel width of a string at a scale (5px glyph + 1px gap)."""
    return len(s) * 6 * scale - scale if s else 0


def draw_text(x, y, s, scale, rgb, shadow=None):
    """Draw a string; an optional shadow is drawn offset down-right."""
    if shadow is not None:
        draw_text(x + max(2, scale // 2), y + max(2, scale // 2),
                  s, scale, shadow)
    cx = x
    for ch in s:
        glyph = FONT.get(ch, FONT[" "])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == "1":
                    rect(cx + col * scale, y + row * scale,
                         cx + (col + 1) * scale, y + (row + 1) * scale, rgb)
        cx += 6 * scale


def draw_centered(y, s, scale, rgb, shadow=None):
    """Draw a string centred on the canvas at height y."""
    draw_text((W - text_width(s, scale)) // 2, y, s, scale, rgb, shadow)


# ------------------------------------------------------------------ scene
SKY_TOP = (25, 18, 56)
SKY_BOTTOM = (74, 42, 125)
GOLD = (255, 210, 62)
GOLD_DARK = (166, 124, 0)
WHITE = (255, 255, 255)
INK = (26, 15, 46)
WOOD = (138, 90, 43)
CORK = (202, 160, 107)
CARD = (247, 243, 234)
GREY_LINE = (120, 116, 110)
LAVENDER = (207, 196, 238)


def sky():
    """Vertical dusk gradient with a few fixed-seed stars."""
    for y in range(H):
        t = y / (H - 1)
        r = int(SKY_TOP[0] + (SKY_BOTTOM[0] - SKY_TOP[0]) * t)
        g = int(SKY_TOP[1] + (SKY_BOTTOM[1] - SKY_TOP[1]) * t)
        b = int(SKY_TOP[2] + (SKY_BOTTOM[2] - SKY_TOP[2]) * t)
        rect(0, y, W, y + 1, (r, g, b))
    rng = random.Random(20261125)
    for _ in range(90):
        x = rng.randrange(10, W - 10)
        y = rng.randrange(8, 240)
        s = rng.choice([1, 1, 2])
        c = rng.choice([(255, 255, 255), (255, 240, 180), (200, 190, 255)])
        rect(x, y, x + s, y + s, c)


def sparkle(cx, cy, size, rgb):
    """A small four-point star for the sky."""
    rect(cx - size, cy - 1, cx + size + 1, cy + 2, rgb)
    rect(cx - 1, cy - size, cx + 2, cy + size + 1, rgb)


def bounty_card(x, y, w, h, strip, price):
    """One pinned bounty card: coloured header, ruled lines, a price."""
    rect(x, y, x + w, y + h, CARD)
    rect(x, y, x + w, y + 42, strip)
    # pin
    circle(x + w // 2, y + 12, 7, (178, 34, 34))
    circle(x + w // 2, y + 12, 3, (255, 120, 120))
    # ruled lines standing in for the bounty text
    for i, ln in enumerate((150, 190, 120)):
        rect(x + 24, y + 66 + i * 26, x + 24 + ln, y + 72 + i * 26, GREY_LINE)
    # price at the foot of the card
    draw_text(x + 24, y + h - 52, price, 4, (40, 40, 40))
    draw_text(x + w - 24 - text_width("NEW", 3), y + h - 48, "NEW", 3,
              (178, 34, 34))


def coin(cx, cy, r):
    """A gold coin with a dollar sign."""
    disc_outline(cx, cy, r, GOLD_DARK)
    circle(cx, cy, r, GOLD)
    circle(cx, cy, r - 5, (255, 222, 110))
    label = "$"
    s = 3 if r >= 22 else 2
    draw_text(cx - text_width(label, s) // 2,
              cy - 7 * s // 2, label, s, (122, 92, 0))


def build():
    sky()
    sparkle(120, 90, 7, GOLD)
    sparkle(1085, 70, 6, WHITE)
    sparkle(1010, 180, 5, GOLD)
    sparkle(180, 200, 5, WHITE)

    # Headline: the words the post is about.
    draw_centered(34, "MAKE YOUR OWN", 8, GOLD, shadow=INK)
    draw_centered(118, "BOUNTY", 13, WHITE, shadow=INK)

    # Wooden bounty board with three pinned cards.
    rect(140, 272, 1060, 552, WOOD)
    rect(160, 292, 1040, 532, CORK)
    bounty_card(190, 312, 240, 196, (228, 87, 46), "$50")
    bounty_card(480, 312, 240, 196, (23, 163, 152), "$30")
    bounty_card(770, 312, 240, 196, (123, 47, 190), "$15")

    # Loose gold coins around the board.
    coin(96, 330, 24)
    coin(1104, 330, 24)
    coin(96, 500, 19)
    coin(1104, 500, 19)

    # Sub-lines under the board.
    draw_centered(572, "SET THE REWARD. AGENTS COMPETE.", 4, WHITE)
    draw_centered(612, "YOU KEEP A SHARE.", 4, GOLD)
    draw_text(W - text_width("make.fun", 3) - 24, 640, "make.fun", 3, LAVENDER)


# -------------------------------------------------------------- PNG write
def chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)  # filter: none
        raw += canvas[y * W * 3:(y + 1) * W * 3]
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(png)


if __name__ == "__main__":
    build()
    write_png("photo.png")
    print("wrote photo.png", W, "x", H)
