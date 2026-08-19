"""Generate LiftLog PWA icons: dark rounded tile + green barbell mark."""
from PIL import Image, ImageDraw

BG = (13, 15, 18, 255)          # near-black, matches --bg-0
ACCENT = (44, 224, 139, 255)    # #2CE08B
ACCENT_HI = (124, 245, 174, 255)

def rounded_tile(size, radius_frac=0.22):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = int(size * radius_frac)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=BG)
    return img, d

def draw_barbell(d, size):
    cx, cy = size / 2, size / 2
    bar_w = size * 0.72          # total barbell width
    bar_h = size * 0.055         # bar thickness
    x0 = cx - bar_w / 2
    x1 = cx + bar_w / 2
    # bar
    d.rounded_rectangle([x0, cy - bar_h / 2, x1, cy + bar_h / 2],
                        radius=bar_h / 2, fill=ACCENT_HI)
    # plates: outer (tall) and inner (taller) on each side
    plate_w = size * 0.075
    inner_h = size * 0.42
    outer_h = size * 0.30
    gap = size * 0.02
    for side in (-1, 1):
        edge = cx + side * bar_w / 2
        ox0 = edge - plate_w if side == 1 else edge
        d.rounded_rectangle([ox0, cy - outer_h / 2, ox0 + plate_w, cy + outer_h / 2],
                            radius=plate_w * 0.4, fill=ACCENT)
        ix_edge = edge - side * (plate_w + gap)
        ix0 = ix_edge - plate_w if side == 1 else ix_edge
        d.rounded_rectangle([ix0, cy - inner_h / 2, ix0 + plate_w, cy + inner_h / 2],
                            radius=plate_w * 0.4, fill=ACCENT)

def make(size, path, full_bleed=False):
    if full_bleed:
        # apple-touch-icon: iOS rounds corners itself, needs opaque square
        img = Image.new("RGBA", (size, size), BG)
        d = ImageDraw.Draw(img)
    else:
        img, d = rounded_tile(size)
    draw_barbell(d, size)
    img.save(path)
    print("wrote", path)

import os
os.makedirs("icons", exist_ok=True)
make(512, "icons/icon-512.png")
make(192, "icons/icon-192.png")
make(180, "icons/apple-touch-icon.png", full_bleed=True)
# maskable: same mark but smaller, inside full-bleed safe zone
img = Image.new("RGBA", (512, 512), BG)
d = ImageDraw.Draw(img)
sub = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
sd = ImageDraw.Draw(sub)
draw_barbell(sd, 400)
img.paste(sub, (56, 56), sub)
img.save("icons/icon-maskable-512.png")
print("wrote icons/icon-maskable-512.png")
