"""LiftLog PWA icons v2 (Liquid Glass, v9.2) — indigo-aurora tile + glassy green barbell.

Regenerates icons/*.png. iOS caches home-screen icons hard: after shipping, the phone
may need the app removed + re-added to Home Screen to show the new icon.
"""
from PIL import Image, ImageChops, ImageDraw, ImageFilter

ACCENT_HI = (140, 247, 183)   # top of the glass mark
ACCENT_LO = (23, 185, 160)    # bottom of the glass mark
GLOW = (44, 224, 139)         # #2CE08B


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))


def vgrad(size, top, bot):
    img = Image.new("RGB", (size, size))
    d = ImageDraw.Draw(img)
    for y in range(size):
        d.line([(0, y), (size, y)], fill=lerp(top, bot, y / size))
    return img


def aurora_bg(size):
    """Deep indigo gradient + blurred teal/violet/pink blobs — the app's aurora."""
    base = vgrad(size, (15, 18, 36), (8, 9, 16))
    glow = Image.new("RGB", (size, size), (0, 0, 0))
    g = ImageDraw.Draw(glow)

    def blob(cx, cy, r, col):
        g.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)

    blob(size * 0.20, size * 0.12, size * 0.46, (18, 118, 104))  # teal, top-left
    blob(size * 0.88, size * 0.92, size * 0.50, (58, 48, 124))   # violet, bottom-right
    blob(size * 0.98, size * 0.22, size * 0.22, (52, 24, 42))    # faint pink, right edge
    glow = glow.filter(ImageFilter.GaussianBlur(size * 0.15))
    return ImageChops.add(base, glow).convert("RGBA")


def mark_mask(size, scale=1.0):
    """The barbell silhouette as an L mask."""
    m = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(m)
    cx = cy = size / 2
    bw = size * 0.72 * scale
    bh = size * 0.058 * scale
    d.rounded_rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2],
                        radius=bh / 2, fill=255)
    pw = size * 0.078 * scale
    inner_h = size * 0.44 * scale
    outer_h = size * 0.31 * scale
    gap = size * 0.022 * scale
    for side in (-1, 1):
        edge = cx + side * bw / 2
        x0 = edge - pw if side == 1 else edge
        d.rounded_rectangle([x0, cy - outer_h / 2, x0 + pw, cy + outer_h / 2],
                            radius=pw * 0.42, fill=255)
        ie = edge - side * (pw + gap)
        x0 = ie - pw if side == 1 else ie
        d.rounded_rectangle([x0, cy - inner_h / 2, x0 + pw, cy + inner_h / 2],
                            radius=pw * 0.42, fill=255)
    return m


def glass_tile(size, mark_scale=1.0):
    """Square (unrounded) tile: aurora bg, glow, gradient mark, specular + sheen."""
    img = aurora_bg(size)
    mm = mark_mask(size, mark_scale)

    # soft green glow under the mark
    halo = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    halo.paste(Image.new("RGBA", (size, size), GLOW + (150,)), (0, 0),
               mm.filter(ImageFilter.GaussianBlur(size * 0.06)))
    img = Image.alpha_composite(img, halo)

    # the mark itself — glass gradient mapped across the MARK's own band (bright top
    # edge -> deep teal bottom), not the whole tile, so the glass reads at icon size
    band_top = size / 2 - size * 0.44 * mark_scale / 2
    band_h = size * 0.44 * mark_scale
    grad = Image.new("RGB", (size, size))
    gd = ImageDraw.Draw(grad)
    for y in range(size):
        t = min(1, max(0, (y - band_top) / band_h))
        gd.line([(0, y), (size, y)], fill=lerp(ACCENT_HI, ACCENT_LO, t))
    mk = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    mk.paste(grad.convert("RGBA"), (0, 0), mm)
    img = Image.alpha_composite(img, mk)

    # specular: white light across the top third of the mark band; a soft dark shade
    # inside its bottom quarter gives the pane thickness
    spec = Image.new("L", (size, size), 0)
    sd = ImageDraw.Draw(spec)
    for y in range(size):
        t = (y - band_top) / band_h
        if 0 <= t < 0.38:
            sd.line([(0, y), (size, y)], fill=int(135 * (1 - t / 0.38)))
    spec = ImageChops.multiply(spec, mm)
    img.paste(Image.new("RGBA", (size, size), (255, 255, 255, 255)), (0, 0), spec)
    shade = Image.new("L", (size, size), 0)
    hd2 = ImageDraw.Draw(shade)
    for y in range(size):
        t = (y - band_top) / band_h
        if 0.72 < t <= 1:
            hd2.line([(0, y), (size, y)], fill=int(70 * (t - 0.72) / 0.28))
    shade = ImageChops.multiply(shade, mm)
    img.paste(Image.new("RGBA", (size, size), (8, 40, 34, 255)), (0, 0), shade)

    # glass sheen across the whole pane's top + a hairline top rim light
    sheen = Image.new("L", (size, size), 0)
    hd = ImageDraw.Draw(sheen)
    top = size * 0.42
    for y in range(int(top)):
        hd.line([(0, y), (size, y)], fill=int(22 * (1 - y / top)))
    img.paste(Image.new("RGBA", (size, size), (255, 255, 255, 255)), (0, 0), sheen)
    rim = ImageDraw.Draw(img)
    rim.line([(size * 0.06, 1), (size * 0.94, 1)], fill=(255, 255, 255, 46),
             width=max(2, size // 256))
    return img


def rounded(img, rfrac=0.23):
    size = img.size[0]
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1],
                                           radius=int(size * rfrac), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


import os
os.makedirs("icons", exist_ok=True)

master = glass_tile(1024)
rounded(master).resize((512, 512), Image.LANCZOS).save("icons/icon-512.png")
rounded(master).resize((192, 192), Image.LANCZOS).save("icons/icon-192.png")
# apple-touch-icon: iOS rounds the corners itself — ship the full-bleed square
master.convert("RGB").resize((180, 180), Image.LANCZOS).save("icons/apple-touch-icon.png")
# maskable: full-bleed with the mark pulled into the safe zone
glass_tile(1024, mark_scale=0.74).convert("RGB").resize((512, 512), Image.LANCZOS) \
    .save("icons/icon-maskable-512.png")
for f in ("icon-512", "icon-192", "apple-touch-icon", "icon-maskable-512"):
    print("wrote icons/" + f + ".png")
