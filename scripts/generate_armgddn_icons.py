#!/usr/bin/env python3
"""Generate ARMGDDN mushroom-skull icons for the drive (gdrive) and ftp
remotes.

This stylised icon is meant as a stand-in for the kind of mushroom-cloud
skull mascot the user wants on their gdrive and ftp tabs. Re-run this
script if you want to regenerate the PNGs from scratch.
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = Path(__file__).resolve().parent.parent
ICON_DIR = REPO_ROOT / "src" / "images" / "remotes_icons"
SIZE = 320
ORANGE = (255, 110, 30, 255)
ORANGE_LIGHT = (255, 165, 60, 255)
SKULL = (220, 220, 215, 255)
SKULL_SHADOW = (130, 130, 130, 255)
EYE = (255, 70, 0, 255)
BLACK = (0, 0, 0, 255)
TRANSPARENT = (0, 0, 0, 0)


def draw_burst(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    """Radial spike pattern around the centre."""
    spikes = 18
    inner = SIZE * 0.34
    outer = SIZE * 0.46
    for i in range(spikes):
        angle = (i / spikes) * 2 * math.pi
        x1 = cx + math.cos(angle) * inner
        y1 = cy + math.sin(angle) * inner
        x2 = cx + math.cos(angle) * outer
        y2 = cy + math.sin(angle) * outer
        draw.line([(x1, y1), (x2, y2)], fill=ORANGE, width=6)
        # smaller dot near the tip
        dot_x = cx + math.cos(angle) * (outer + 8)
        dot_y = cy + math.sin(angle) * (outer + 8)
        draw.ellipse(
            [dot_x - 4, dot_y - 4, dot_x + 4, dot_y + 4], fill=ORANGE
        )


def draw_mushroom_cloud(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    """Cluster of overlapping orange ellipses to form the mushroom cap."""
    cap_radius = SIZE * 0.30
    base_y = cy - SIZE * 0.04

    # Outer cap ring
    cap_lobes = [
        (-1.00, -0.20, 0.55, 0.55),
        (-0.65, -0.55, 0.55, 0.55),
        (-0.25, -0.75, 0.55, 0.55),
        (0.20, -0.78, 0.55, 0.55),
        (0.60, -0.60, 0.55, 0.55),
        (0.95, -0.25, 0.55, 0.55),
        (-0.45, -0.10, 0.55, 0.55),
        (0.05, -0.30, 0.65, 0.65),
        (0.45, -0.10, 0.55, 0.55),
    ]
    for ox, oy, w, h in cap_lobes:
        rx = cap_radius * w
        ry = cap_radius * h
        x = cx + cap_radius * ox
        y = base_y + cap_radius * oy
        draw.ellipse([x - rx, y - ry, x + rx, y + ry], fill=ORANGE)

    # Highlight lobes
    for ox, oy, w, h in [
        (-0.55, -0.45, 0.35, 0.35),
        (-0.10, -0.65, 0.35, 0.35),
        (0.40, -0.50, 0.35, 0.35),
        (-0.20, -0.30, 0.30, 0.30),
        (0.20, -0.20, 0.25, 0.25),
    ]:
        rx = cap_radius * w
        ry = cap_radius * h
        x = cx + cap_radius * ox
        y = base_y + cap_radius * oy
        draw.ellipse([x - rx, y - ry, x + rx, y + ry], fill=ORANGE_LIGHT)


def draw_skull(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    """Cartoon skull centred at (cx, cy)."""
    skull_w = SIZE * 0.36
    skull_h = SIZE * 0.34
    head_top = cy - skull_h * 0.10
    # main cranium
    draw.ellipse(
        [cx - skull_w, head_top - skull_h, cx + skull_w, head_top + skull_h],
        fill=SKULL,
        outline=BLACK,
        width=4,
    )
    # jaw
    jaw_w = skull_w * 0.78
    jaw_h = skull_h * 0.40
    jaw_y = head_top + skull_h * 0.55
    draw.ellipse(
        [cx - jaw_w, jaw_y - jaw_h, cx + jaw_w, jaw_y + jaw_h],
        fill=SKULL,
        outline=BLACK,
        width=4,
    )

    # eye sockets
    eye_dx = skull_w * 0.45
    eye_dy = head_top - skull_h * 0.05
    eye_r = skull_w * 0.25
    for sign in (-1, 1):
        x = cx + sign * eye_dx
        draw.ellipse(
            [x - eye_r, eye_dy - eye_r, x + eye_r, eye_dy + eye_r],
            fill=BLACK,
            outline=BLACK,
        )
        # glowing pupil
        pr = eye_r * 0.45
        draw.ellipse(
            [x - pr, eye_dy - pr, x + pr, eye_dy + pr], fill=EYE
        )

    # nose
    nose_w = skull_w * 0.10
    nose_h = skull_h * 0.18
    nose_y = head_top + skull_h * 0.20
    draw.polygon(
        [
            (cx, nose_y - nose_h),
            (cx - nose_w, nose_y + nose_h),
            (cx + nose_w, nose_y + nose_h),
        ],
        fill=BLACK,
    )

    # teeth
    teeth_w = skull_w * 0.85
    teeth_y = head_top + skull_h * 0.50
    teeth_h = skull_h * 0.20
    draw.rectangle(
        [cx - teeth_w * 0.55, teeth_y, cx + teeth_w * 0.55, teeth_y + teeth_h],
        fill=SKULL,
        outline=BLACK,
        width=3,
    )
    teeth_count = 6
    for i in range(1, teeth_count):
        x = cx - teeth_w * 0.55 + (teeth_w * 1.10 / teeth_count) * i
        draw.line(
            [(x, teeth_y), (x, teeth_y + teeth_h)], fill=BLACK, width=2
        )

    # subtle cheek shadow
    shadow_radius = skull_w * 0.18
    for sign in (-1, 1):
        sx = cx + sign * skull_w * 0.55
        sy = head_top + skull_h * 0.30
        draw.ellipse(
            [
                sx - shadow_radius,
                sy - shadow_radius,
                sx + shadow_radius,
                sy + shadow_radius,
            ],
            fill=SKULL_SHADOW,
        )


def render_icon() -> Image.Image:
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT)

    # Soft halo background so the icon reads on both light and dark themes.
    halo = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT)
    halo_draw = ImageDraw.Draw(halo)
    halo_draw.ellipse(
        [SIZE * 0.10, SIZE * 0.10, SIZE * 0.90, SIZE * 0.90],
        fill=(255, 90, 20, 90),
    )
    halo = halo.filter(ImageFilter.GaussianBlur(radius=12))
    img.alpha_composite(halo)

    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2
    draw_burst(draw, cx, cy)
    draw_mushroom_cloud(draw, cx, cy)
    draw_skull(draw, cx, int(cy + SIZE * 0.18))
    return img


def render_inverted_icon(base: Image.Image) -> Image.Image:
    """Variant for the 'white' icon theme: lift midtones to keep the
    icon readable on dark UI chrome."""
    inverted = base.copy()
    pixels = inverted.load()
    for y in range(inverted.height):
        for x in range(inverted.width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            # Brighten dark pixels so the outline reads on dark themes.
            r = min(255, int(r * 0.95) + 30)
            g = min(255, int(g * 0.95) + 30)
            b = min(255, int(b * 0.95) + 30)
            pixels[x, y] = (r, g, b, a)
    return inverted


def main() -> None:
    icon = render_icon()
    inverted = render_inverted_icon(icon)

    targets = [
        ("drive.png", icon),
        ("drive_inv.png", inverted),
        ("ftp.png", icon),
        ("ftp_inv.png", inverted),
    ]

    ICON_DIR.mkdir(parents=True, exist_ok=True)
    for name, image in targets:
        out = ICON_DIR / name
        image.save(out, format="PNG")
        print(f"wrote {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
