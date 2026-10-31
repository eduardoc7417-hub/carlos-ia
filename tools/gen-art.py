#!/usr/bin/env python3
"""Gera logo e papéis de parede próprios do Carlos OS Aurora. Toda a arte sai deste script."""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "live", "includes.chroot")
WALL = os.path.join(ROOT, "usr/share/backgrounds/carlos")
FONT = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
W, H = 2560, 1600

# nome: (seed, céu em cima, céu embaixo, cores da aurora, estrelas)
WALLPAPERS = {
    "aurora-noite": (7, "#050816", "#0d1b3a", ["#2ef2b0", "#3a8bff", "#8a5cff"], True),
    "aurora-verde": (11, "#03110f", "#08302c", ["#6dff9c", "#1fd8a4", "#35b6ff"], True),
    "aurora-rosa": (23, "#120620", "#2b0f3f", ["#ff5fa8", "#a65cff", "#4fa8ff"], True),
    "aurora-ambar": (31, "#170a12", "#3a1a22", ["#ffb347", "#ff6f61", "#c04dff"], True),
    "alvorecer": (41, "#6d8fd8", "#fbd9c8", ["#ffffff", "#ffc2d6", "#b7c8ff"], False),
    "manha": (47, "#a9d4f5", "#eef6fb", ["#ffffff", "#9fe3e0", "#c4d2ff"], False),
    "vidro-azul": (53, "#071a3d", "#0f5cc0", ["#5fd0ff", "#a9e6ff", "#3f7bff"], False),
    "grafite": (59, "#101216", "#23272f", ["#7f8ea3", "#4f8cff", "#a0a8b5"], False),
}

# nome: (seed, fundo em cima, fundo embaixo, pétala escura, pétala média, brilho)
BLOOMS = {
    "flor-azul": (101, "#0a2a66", "#0f5fc4", "#0a3ea8", "#2f9bff", "#a8e4ff"),
    "flor-clara": (103, "#dcecff", "#f6fbff", "#3f8cf0", "#8fd0ff", "#ffffff"),
    "flor-violeta": (107, "#1a0d40", "#42209a", "#4a1fb8", "#a05cff", "#f0c8ff"),
    "flor-coral": (109, "#3a0d1e", "#a02c3c", "#c8324a", "#ff8a5c", "#ffe0b8"),
    "flor-esmeralda": (113, "#04261f", "#0b6b58", "#08806a", "#3fe0b0", "#d0fff0"),
    "flor-grafite": (127, "#0c0e12", "#1c2028", "#2a3442", "#6a86a8", "#d8e6f5"),
}


def rgb(value):
    return np.array([int(value[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.float32) / 255


def aurora(width, height, seed, top, bottom, colors, stars):
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:height, 0:width].astype(np.float32)
    u, v = x / width, y / height
    image = rgb(top) * (1 - v[..., None]) + rgb(bottom) * v[..., None]
    if stars:
        field = rng.random((height, width)) > 0.9994
        image += (field * rng.uniform(0.3, 1, (height, width)) * (1 - v) ** 2)[..., None]
    for index, color in enumerate(colors * 2):
        phases = rng.uniform(0, 6.28, 3)
        freqs = rng.uniform(1.2, 4.5, 3)
        center = 0.28 + 0.1 * index + sum(
            0.07 / (k + 1) * np.sin(freqs[k] * 6.28 * u + phases[k]) for k in range(3))
        offset = v - center
        # Sobe longa e desce curta, como a cortina de uma aurora.
        curtain = np.exp(-(offset / np.where(offset < 0, 0.2, 0.045)) ** 2)
        rays = 0.88 + 0.12 * np.sin(u * rng.uniform(28, 55) + 2.5 * np.sin(u * 7 + phases[0]))
        image += curtain[..., None] * (rays * rng.uniform(0.22, 0.42))[..., None] * rgb(color)
    image = 1 - np.exp(-1.6 * image)
    image += rng.normal(0, 1.2 / 255, image.shape)  # evita faixas no degradê
    return Image.fromarray((np.clip(image, 0, 1) * 255).astype(np.uint8))


def smooth(edge0, edge1, value):
    t = np.clip((value - edge0) / (edge1 - edge0), 0, 1)
    return t * t * (3 - 2 * t)


def bloom(width, height, seed, top, bottom, dark, mid, light):
    """Flor abstrata de pétalas translúcidas, em desenho próprio."""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:height, 0:width].astype(np.float32)
    u, v = x / width, y / height
    image = rgb(top) * (1 - v[..., None]) + rgb(bottom) * v[..., None]
    px = (x - width * 0.5) / height
    py = (y - height * 0.5) / height
    count = 11
    order = list(range(count))
    rng.shuffle(order)
    for k in order:
        angle = 6.283 * k / count + rng.uniform(-0.05, 0.05)
        length = rng.uniform(0.36, 0.44)
        wide = rng.uniform(0.17, 0.22)
        along = px * np.cos(angle) + py * np.sin(angle)
        across = -px * np.sin(angle) + py * np.cos(angle)
        t = np.clip(along / length, 0, 1)
        limit = wide * np.sin(np.pi * t) ** 0.72 + 1e-4
        # O corte em t tira os fios finos que sobravam nas pontas da pétala.
        alpha = (1 - smooth(0.97, 1.0, np.abs(across) / limit)) * ((t > 0.002) & (t < 0.998))
        side = np.clip(0.5 + across / (2 * limit), 0, 1)
        tone = (0.15 + 0.85 * t) * (0.55 + 0.45 * side)
        tone = tone[..., None]
        color = rgb(dark) * (1 - tone) + rgb(mid) * tone
        color = color + rgb(light) * (t * side * 0.35)[..., None]
        strength = (alpha * 0.82)[..., None]
        image = image * (1 - strength) + color * strength
    glow = np.exp(-(px ** 2 + py ** 2) / 0.012)[..., None]
    image = image + glow * rgb(light) * 0.5
    image += rng.normal(0, 1.2 / 255, image.shape)
    return Image.fromarray((np.clip(image, 0, 1) * 255).astype(np.uint8))


def mark(size):
    scale = 4
    big = size * scale
    art = aurora(big, big, 7, "#071030", "#102a5c", ["#2ef2b0", "#3a8bff", "#8a5cff"], False).convert("RGBA")
    mask = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, big - 1, big - 1), radius=int(big * 0.23), fill=255)
    art.putalpha(mask)
    draw = ImageDraw.Draw(art)
    stroke = int(big * 0.085)
    peak = (big * 0.5, big * 0.2)
    draw.line([(big * 0.2, big * 0.8), peak, (big * 0.8, big * 0.8)], fill="white", width=stroke, joint="curve")
    draw.line([(big * 0.33, big * 0.6), (big * 0.67, big * 0.6)], fill="white", width=int(stroke * 0.7))
    return art.resize((size, size), Image.LANCZOS)


def main():
    os.makedirs(WALL, exist_ok=True)
    for name, (seed, top, bottom, colors, stars) in WALLPAPERS.items():
        aurora(W, H, seed, top, bottom, colors, stars).save(os.path.join(WALL, name + ".jpg"), quality=90)
    for name, values in BLOOMS.items():
        bloom(W, H, *values).save(os.path.join(WALL, name + ".jpg"), quality=90)
    icon = mark(256)
    for path in ("usr/share/icons/hicolor/256x256/apps/carlos-logo.png", "usr/share/pixmaps/carlos-logo.png"):
        target = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        icon.save(target)
    # Logo com o nome, usado na tela de login.
    font = ImageFont.truetype(FONT, 72)
    text = "Carlos OS Aurora"
    width = int(font.getlength(text))
    banner = Image.new("RGBA", (128 + 36 + width, 128), (0, 0, 0, 0))
    small = mark(128)
    banner.paste(small, (0, 0), small)
    ImageDraw.Draw(banner).text((164, 64), text, font=font, fill="white", anchor="lm")
    banner = banner.resize((banner.width // 2, 64), Image.LANCZOS)
    banner.save(os.path.join(ROOT, "usr/share/pixmaps/carlos-logo-text.png"))
    print("arte gerada:", len(WALLPAPERS) + len(BLOOMS), "papeis de parede")


if __name__ == "__main__":
    sys.exit(main())
