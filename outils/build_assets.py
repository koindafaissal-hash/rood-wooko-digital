#!/usr/bin/env python3
"""Assets finaux ROOD-WOOKO DIGITAL : 5 logotypes animés du client, recadrés,
optimisés (GIF léger), déclinés sur fond clair ET fond transparent (charbon),
+ versions PNG statiques (prefers-reduced-motion)."""
from PIL import Image
import os, glob, numpy as np

SRC = sorted(glob.glob('/workspace/attachments/*/*.gif'))
OUT = '/workspace/rood-wooko-digital/assets/logo'
os.makedirs(OUT, exist_ok=True)

# (fichier source, bande de découpe y, largeur cible, palette couleur)
# bg = couleur du conteneur sur lequel le logo sera posé (fond cuit dans le GIF :
# plus fiable que l'index de transparence du format GIF, qui est limité à 1 bit).
SPECS = {
    'header': dict(src=3, band=(300, 575), w=300, colors=64, bg=(26, 26, 26)),
    'hero':   dict(src=1, band=None,      w=440, colors=64, bg=(255, 255, 255)),
    'buste':  dict(src=0, band=(0, 576),   w=360, colors=64, bg=(255, 255, 255)),
    'avatar': dict(src=4, band=None,      w=260, colors=64, bg=(255, 255, 255)),
    'dots':   dict(src=2, band=(0, 576),   w=300, colors=48, bg=(255, 255, 255)),
}

def load(idx):
    im = Image.open(SRC[idx]); out = []
    for i in range(im.n_frames):
        im.seek(i); out.append(im.convert('RGB'))
    return out

def make_transparent(fr):
    """Le blanc devient transparent ; les couleurs de marque restent opaques.
    Seuil doux sur le blanc pur (anti-aliasing), opaque dès que le pixel s'en éloigne."""
    a = np.array(fr).astype(np.int16)
    mn = a.min(axis=2)                       # canal le plus bas
    alpha = np.clip((248 - mn) * 255.0 / 23.0, 0, 255).astype(np.uint8)
    # garantit l'opacité du cœur des lettres cuivrées
    alpha[mn < 225] = 255
    rgba = np.dstack([a.astype(np.uint8), alpha])
    return Image.fromarray(rgba, 'RGBA')

def content_bbox(frames, thresh=22):
    x0 = y0 = 10**9; x1 = y1 = -1
    for fr in frames:
        m = fr.convert('L').point(lambda p: 255 if p < (255 - thresh) else 0)
        bb = m.getbbox()
        if bb:
            x0 = min(x0, bb[0]); y0 = min(y0, bb[1]); x1 = max(x1, bb[2]); y1 = max(y1, bb[3])
    return (x0, y0, x1, y1)

for name, s in SPECS.items():
    frames = load(s['src'])
    if s['band']:
        y0, y1 = s['band']
        frames = [f.crop((0, y0, f.size[0], y1)) for f in frames]
    bb = content_bbox(frames)
    frames = [f.crop(bb) for f in frames]
    w, h = frames[0].size
    nh = max(1, int(round(h * s['w'] / w)))
    frames = [f.resize((s['w'], nh), Image.LANCZOS) for f in frames]

    bg = s['bg']
    # 1. le blanc du logo devient transparent, puis on cuit le fond du conteneur
    frames_a = [make_transparent(f) for f in frames]
    composed = []
    for f in frames_a:
        layer = Image.new('RGBA', f.size, bg + (255,))
        composed.append(Image.alpha_composite(layer, f).convert('RGB'))

    gif_frames = [f.convert('P', palette=Image.ADAPTIVE, colors=s['colors'],
                            dither=Image.Dither.FLOYDSTEINBERG) for f in composed]
    gif_frames[0].save(os.path.join(OUT, name + '.gif'), save_all=True,
                       append_images=gif_frames[1:], duration=170, loop=0,
                       optimize=True, disposal=2)

    # PNG statique (repli prefers-reduced-motion) : frame la plus « neutre »
    # frame statique : celle où l'encre est la plus faible = logotype le plus lisible
    best, score = 0, 10**9
    for i, f in enumerate(frames_a):
        al = np.array(f)[:, :, 3]
        dark = int((al > 40).sum())
        if dark < score:
            score, best = dark, i
    layer = Image.new('RGBA', frames_a[best].size, bg + (255,))
    Image.alpha_composite(layer, frames_a[best]).convert('RGB').save(
        os.path.join(OUT, name + '-static.png'), optimize=True)

    gif_sz = os.path.getsize(os.path.join(OUT, name + '.gif')) / 1024
    png_sz = os.path.getsize(os.path.join(OUT, name + '-static.png')) / 1024
    print(f'{name:8s} src#{s["src"]} {w}x{h} -> {s["w"]}x{nh}  '
          f'{gif_sz:6.1f} Ko GIF / {png_sz:6.1f} Ko PNG  fond={bg}')
