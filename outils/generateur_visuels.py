#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Générateur de visuels SVG locaux pour ROOD-WOOKO DIGITAL.
Aucun asset externe : tout est produit ici, en SVG vectoriel.
Langage graphique : cuivre/bronze (le logotype), rouge profond, noir charbon,
or, plus le motif « masque » qui est l'ADN de la marque.
"""
import os, math


def esc(t):
    """Échappe les caractères XML interdits."""
    return (str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;'))

ROOT = '/workspace/rood-wooko-digital/assets/img'
os.makedirs(ROOT, exist_ok=True)

CUIVRE   = '#B87333'
CUIVRE_C = '#D9A06B'
CUIVRE_F = '#7C4A1E'
ROUGE    = '#C0392B'
ROUGE_F  = '#8E2A20'
CHARBON  = '#1A1A1A'
OR       = '#F1C40F'
CREME    = '#F5F5F3'
BLANC    = '#FFFFFF'


# --------------------------------------------------------------------------
# Masque stylisé (signature de marque) — dessinable à toute échelle
# --------------------------------------------------------------------------
def masque(cx, cy, h, opacite=0.14, couleur=CREME, simple=False):
    """Masque bronze stylisé : visage, oreilles, yeux, crête de doigts."""
    s = h / 240.0
    # la silhouette occupe environ de -226s (crête) à +120s (menton) :
    # on translate pour que son centre visuel tombe sur (cx, cy)
    g = [f'<g transform="translate({cx - 100*s:.1f},{cy + 53*s:.1f}) scale({s:.4f})" '
         f'fill="{couleur}" opacity="{opacite}">']
    # crête : 7 doigts arrondis
    for i, (ang, ln, rx) in enumerate([(-42, 92, 15), (-27, 104, 16), (-12, 110, 17),
                                       (0, 112, 17), (12, 110, 17), (27, 104, 16),
                                       (42, 92, 15)]):
        x = 100 + rx * 0.9
        g.append(f'<rect x="{x - rx/2:.1f}" y="{6 - ln:.1f}" width="{rx}" height="{ln}" '
                 f'rx="{rx/2:.1f}" ry="{rx/2:.1f}" transform="rotate({ang} {x:.1f} 60)"/>')
    # visage
    g.append('<path d="M100 26 C148 26 176 66 176 118 C176 166 142 212 100 240 '
             'C58 212 24 166 24 118 C24 66 52 26 100 26 Z"/>')
    # oreilles
    g.append('<ellipse cx="20" cy="122" rx="16" ry="22"/>')
    g.append('<ellipse cx="180" cy="122" rx="16" ry="22"/>')
    if simple:
        g.append('</g>')
        return ''.join(g)
    # yeux (en amande, évidés)
    g.append(f'<path d="M56 104 C70 88 92 88 100 100 C88 114 68 116 56 104 Z" fill="{CHARBON}" opacity="0.30"/>')
    g.append(f'<path d="M144 104 C130 88 108 88 100 100 C112 114 132 116 144 104 Z" fill="{CHARBON}" opacity="0.30"/>')
    # nez + bouche (en creux)
    g.append(f'<path d="M100 108 L86 152 C93 160 107 160 114 152 Z" fill="{CHARBON}" opacity="0.22"/>')
    g.append(f'<path d="M78 176 C90 187 110 187 122 176 L116 186 C104 192 96 192 84 186 Z" fill="{CHARBON}" opacity="0.30"/>')
    g.append('</g>')
    return ''.join(g)


def embleme(cx, cy, r, couleur=CUIVRE, opacite=1.0, initiales='RW'):
    """Écusson circulaire avec les initiales."""
    return (f'<g opacity="{opacite}"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" '
            f'stroke="{couleur}" stroke-width="{r*0.06:.2f}" opacity="0.85"/>'
            f'<text x="{cx}" y="{cy + r*0.30:.1f}" font-family="Georgia,serif" font-size="{r*0.62:.1f}" '
            f'font-weight="700" fill="{couleur}" text-anchor="middle" letter-spacing="{r*0.03:.1f}">'
            f'{initiales}</text></g>')


# --------------------------------------------------------------------------
# Motifs de catégorie
# --------------------------------------------------------------------------
def motif_photo(c, s, cx, cy):
    """diaphragme d'appareil photo"""
    p = []
    r = s * 0.30
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.92}" fill="none" stroke="{c["gold"]}" stroke-width="{r*0.07:.2f}" opacity="0.95"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.58}" fill="{c["red"]}" opacity="0.92"/>')
    # lamelles
    for i in range(6):
        a = math.radians(i * 60 + 15)
        x1 = cx + r * 0.58 * math.cos(a); y1 = cy + r * 0.58 * math.sin(a)
        x2 = cx + r * 0.92 * math.cos(a + 0.55); y2 = cy + r * 0.92 * math.sin(a + 0.55)
        p.append(f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{c["gold"]}" '
                 f'stroke-width="{r*0.05:.2f}" opacity="0.9" stroke-linecap="round"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.20}" fill="{c["cream"]}" opacity="0.95"/>')
    return ''.join(p)


def motif_design(c, s, cx, cy):
    """plume de stylo + courbe de Bézier + nuancier"""
    w = s * 0.52
    p = [f'<path d="M{cx} {cy - w*0.62} L{cx + w*0.30} {cy + w*0.45} L{cx - w*0.30} {cy + w*0.45} Z" '
         f'fill="{c["cream"]}" opacity="0.95"/>',
         f'<circle cx="{cx}" cy="{cy - w*0.44}" r="{w*0.11}" fill="{c["red"]}"/>',
         f'<path d="M{cx - w*0.62} {cy + w*0.62} C{cx - w*0.2} {cy - w*0.25}, '
         f'{cx + w*0.25} {cy + w*0.30}, {cx + w*0.66} {cy - w*0.10}" fill="none" '
         f'stroke="{c["gold"]}" stroke-width="{w*0.05:.2f}" stroke-linecap="round" opacity="0.95"/>']
    sw = [(c['red'], -1), (c['gold'], 0), (c['cuivre'], 1)]
    for col, i in sw:
        x = cx - w * 0.58 + i * w * 0.42
        p.append(f'<rect x="{x - w*0.13:.1f}" y="{cy + w*0.58:.1f}" width="{w*0.26:.1f}" '
                 f'height="{w*0.26:.1f}" rx="{w*0.05:.1f}" fill="{col}" opacity="0.92"/>')
    return ''.join(p)


def motif_impression(c, s, cx, cy):
    """piles de supports imprimés + bobine"""
    w = s * 0.60
    p = []
    for i, col in enumerate([c['cuivre'], c['red'], c['gold']]):
        y = cy - w * 0.42 + i * w * 0.20
        p.append(f'<rect x="{cx - w*0.48 + i*w*0.05:.1f}" y="{y:.1f}" width="{w*0.92:.1f}" '
                 f'height="{w*0.30:.1f}" rx="{w*0.04:.1f}" fill="{col}" opacity="{0.92 - i*0.12:.2f}"/>')
        p.append(f'<rect x="{cx - w*0.36 + i*w*0.05:.1f}" y="{y + w*0.09:.1f}" width="{w*0.50:.1f}" '
                 f'height="{w*0.06:.1f}" rx="{w*0.03:.1f}" fill="{c["cream"]}" opacity="0.55"/>')
    p.append(f'<circle cx="{cx + w*0.52}" cy="{cy + w*0.30}" r="{w*0.22}" fill="none" '
             f'stroke="{c["cream"]}" stroke-width="{w*0.06:.2f}" opacity="0.9"/>')
    p.append(f'<circle cx="{cx + w*0.52}" cy="{cy + w*0.30}" r="{w*0.07}" fill="{c["cream"]}" opacity="0.9"/>')
    return ''.join(p)


def motif_web(c, s, cx, cy):
    """fenêtre de navigateur + appareils"""
    w = s * 0.66
    p = [f'<rect x="{cx - w*0.5:.1f}" y="{cy - w*0.42:.1f}" width="{w:.1f}" height="{w*0.72:.1f}" '
         f'rx="{w*0.06:.1f}" fill="{c["cream"]}" opacity="0.95"/>',
         f'<rect x="{cx - w*0.5:.1f}" y="{cy - w*0.42:.1f}" width="{w:.1f}" height="{w*0.13:.1f}" '
         f'rx="{w*0.06:.1f}" fill="{c["red"]}" opacity="0.95"/>']
    for i in range(3):
        p.append(f'<circle cx="{cx - w*0.40 + i*w*0.09:.1f}" cy="{cy - w*0.355:.1f}" '
                 f'r="{w*0.022:.1f}" fill="{c["cream"]}" opacity="0.85"/>')
    for i, (yy, ww) in enumerate([(-0.18, 0.60), (-0.02, 0.44), (0.14, 0.52)]):
        p.append(f'<rect x="{cx - w*0.40:.1f}" y="{cy + w*yy:.1f}" width="{w*ww:.1f}" '
                 f'height="{w*0.07:.1f}" rx="{w*0.035:.1f}" fill="{c["cuivre"]}" opacity="0.85"/>')
    p.append(f'<rect x="{cx + w*0.30:.1f}" y="{cy + w*0.10:.1f}" width="{w*0.34:.1f}" '
             f'height="{w*0.52:.1f}" rx="{w*0.05:.1f}" fill="{c["gold"]}" opacity="0.92"/>')
    return ''.join(p)


def motif_evenement(c, s, cx, cy):
    """scène, sono et foule (stades, mariages)"""
    w = s * 0.62
    p = [f'<rect x="{cx - w*0.10:.1f}" y="{cy - w*0.70:.1f}" width="{w*0.20:.1f}" height="{w*0.55:.1f}" '
         f'rx="{w*0.04:.1f}" fill="{c["cream"]}" opacity="0.92"/>',
         f'<path d="M{cx - w*0.34} {cy - w*0.62} L{cx + w*0.34} {cy - w*0.62} L{cx + w*0.18} {cy - w*0.20} '
         f'L{cx - w*0.18} {cy - w*0.20} Z" fill="{c["gold"]}" opacity="0.95"/>',
         f'<circle cx="{cx}" cy="{cy + w*0.30}" r="{w*0.20}" fill="{c["red"]}" opacity="0.92"/>']
    for i, dx in enumerate((-0.26, 0.26)):
        p.append(f'<circle cx="{cx + w*dx:.1f}" cy="{cy + w*0.36:.1f}" r="{w*0.11:.1f}" '
                 f'fill="{c["cream"]}" opacity="0.85"/>')
    for i in range(7):
        p.append(f'<rect x="{cx - w*0.52 + i*w*0.17:.1f}" y="{cy + w*0.62:.1f}" width="{w*0.10:.1f}" '
                 f'height="{w*0.12:.1f}" rx="{w*0.04:.1f}" fill="{c["cuivre"]}" opacity="0.7"/>')
    return ''.join(p)


MOTIFS = {
    'photo': motif_photo, 'design': motif_design, 'impression': motif_impression,
    'web': motif_web, 'evenement': motif_evenement,
}


# --------------------------------------------------------------------------
# Visuel de catalogue
# --------------------------------------------------------------------------
def visuel_catalogue(slug, titre, categorie, motif, tone, size=(800, 600)):
    W, H = size
    if tone == 'sombre':
        fond1, fond2 = '#2A1210', CHARBON
    elif tone == 'chaleureux':
        fond1, fond2 = '#5A2410', '#241009'
    else:
        fond1, fond2 = '#3A1512', '#141414'
    c = dict(red=ROUGE, gold=OR, cuivre=CUIVRE, cream=CREME)
    rnd = abs(hash(slug)) % 1000 / 1000.0
    cx = W * (0.40 + 0.22 * rnd)
    cy = H * 0.46
    d = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="{esc(titre)}">']
    d.append(f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0" stop-color="{fond1}"/><stop offset="1" stop-color="{fond2}"/>'
             f'</linearGradient>'
             f'<radialGradient id="glow" cx="{cx/W:.2f}" cy="{cy/H:.2f}" r="0.62">'
             f'<stop offset="0" stop-color="{CUIVRE_C}" stop-opacity="0.40"/>'
             f'<stop offset="1" stop-color="{CUIVRE_C}" stop-opacity="0"/></radialGradient>'
             f'<pattern id="trame" width="34" height="34" patternUnits="userSpaceOnUse" '
             f'patternTransform="rotate(32)">'
             f'<line x1="0" y1="0" x2="0" y2="34" stroke="{CREME}" stroke-width="1" stroke-opacity="0.05"/>'
             f'</pattern></defs>')
    d.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    d.append(f'<rect width="{W}" height="{H}" fill="url(#glow)"/>')
    d.append(f'<rect width="{W}" height="{H}" fill="url(#trame)"/>')
    # arcs décoratifs
    for i, r in enumerate((0.30, 0.44, 0.58)):
        d.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{H*r:.0f}" fill="none" '
                 f'stroke="{OR if i==1 else CREME}" stroke-width="{2 if i==1 else 1}" '
                 f'stroke-opacity="{0.30 if i==1 else 0.12}" stroke-dasharray="{18 if i==0 else 0} '
                 f'{14 if i==0 else 0}"/>')
    # filigrane : silhouette du masque, discrète, en bas à droite
    d.append(masque(W * 0.86, H * 0.88, H * 0.66, 0.085, CREME, simple=True))
    d.append(MOTIFS[motif](c, min(W, H), cx, cy))
    # repères de cadrage (clin d'œil photographique)
    for gx, gy, dx, dy in ((24, 24, 1, 1), (W - 24, 24, -1, 1),
                           (24, H - 88, 1, -1), (W - 24, H - 88, -1, -1)):
        d.append(f'<path d="M{gx} {gy + 26*dy} L{gx} {gy} L{gx + 26*dx} {gy}" fill="none" '
                 f'stroke="{CUIVRE_C}" stroke-width="2.5" stroke-opacity="0.75" stroke-linecap="round"/>')
    d.append(embleme(W - 74, 74, 30, CUIVRE_C, 0.55))
    # bandeau de catégorie
    d.append(f'<rect x="0" y="{H-64}" width="{W}" height="64" fill="{CHARBON}" opacity="0.30"/>')
    d.append(f'<rect x="0" y="{H-64}" width="6" height="64" fill="{ROUGE}"/>')
    d.append(f'<text x="26" y="{H-24}" font-family="Georgia,serif" font-size="25" '
             f'fill="{CREME}" opacity="0.92" letter-spacing="1.2">{esc(categorie.upper())}</text>')
    d.append('</svg>')
    return ''.join(d)


# --------------------------------------------------------------------------
# Visuel de bannière (carrousel héro)
# --------------------------------------------------------------------------
def visuel_banniere(slug, titre, sous_titre, accent, size=(1920, 640)):
    W, H = size
    d = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="{esc(titre)}">']
    d.append(f'<defs><linearGradient id="hb" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0" stop-color="{CHARBON}"/><stop offset="0.55" stop-color="#24110F"/>'
             f'<stop offset="1" stop-color="{accent}"/></linearGradient>'
             f'<radialGradient id="hg" cx="0.72" cy="0.35" r="0.55">'
             f'<stop offset="0" stop-color="{CUIVRE_C}" stop-opacity="0.34"/>'
             f'<stop offset="1" stop-color="{CUIVRE_C}" stop-opacity="0"/></radialGradient>'
             f'<pattern id="ht" width="56" height="56" patternUnits="userSpaceOnUse" '
             f'patternTransform="rotate(35)"><line x1="0" y1="0" x2="0" y2="56" stroke="{CREME}" '
             f'stroke-width="1.5" stroke-opacity="0.045"/></pattern></defs>')
    d.append(f'<rect width="{W}" height="{H}" fill="url(#hb)"/>')
    d.append(f'<rect width="{W}" height="{H}" fill="url(#hg)"/>')
    d.append(f'<rect width="{W}" height="{H}" fill="url(#ht)"/>')
    # bande de lisibilité à gauche (le texte du héros se pose dessus)
    d.append(f'<linearGradient id="voile" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0" stop-color="{CHARBON}" stop-opacity="0.92"/>'
             f'<stop offset="0.5" stop-color="{CHARBON}" stop-opacity="0.55"/>'
             f'<stop offset="1" stop-color="{CHARBON}" stop-opacity="0"/></linearGradient>')
    # arcs concentriques à droite
    for i, r in enumerate((150, 250, 360, 480)):
        d.append(f'<circle cx="{W*0.74:.0f}" cy="{H*0.48:.0f}" r="{r}" fill="none" '
                 f'stroke="{OR if i%2 else CUIVRE_C}" stroke-width="{3 if i%2 else 1.5}" '
                 f'stroke-opacity="{0.30 if i%2 else 0.15}"/>')
    # trame de points à l'extrême droite
    for r in range(9):
        for c_ in range(5):
            d.append(f'<circle cx="{W-150 + c_*34:.0f}" cy="{H-150 + r*34:.0f}" r="3" '
                     f'fill="{CREME}" fill-opacity="0.16"/>')
    d.append(f'<circle cx="{W*0.74:.0f}" cy="{H*0.48:.0f}" r="96" fill="{ROUGE}" opacity="0.22"/>')
    d.append(masque(W * 0.74, H * 0.50, H * 0.60, 0.34, CUIVRE_C))
    d.append(f'<rect width="{W}" height="{H}" fill="url(#voile)"/>')
    d.append(f'<rect x="0" y="{H-8}" width="{W}" height="8" fill="{accent}"/>')
    d.append('</svg>')
    return ''.join(d)


# --------------------------------------------------------------------------
# Visuel de catégorie (carte)
# --------------------------------------------------------------------------
def visuel_categorie(slug, titre, motif, tone, size=(520, 360)):
    W, H = size
    fond1, fond2 = {'sombre': ('#2A1210', CHARBON), 'clair': ('#FBF8F4', '#EFE6DA'),
                    'chaleureux': ('#5A2410', '#241009')}.get(tone, ('#2A1210', CHARBON))
    c = dict(red=ROUGE, gold=OR, cuivre=CUIVRE, cream=CREME)
    clair = tone == 'clair'
    d = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="{esc(titre)}">']
    d.append(f'<defs><linearGradient id="cb" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0" stop-color="{fond1}"/><stop offset="1" stop-color="{fond2}"/>'
             f'</linearGradient></defs>')
    d.append(f'<rect width="{W}" height="{H}" fill="url(#cb)"/>')
    d.append(f'<circle cx="{W*0.78:.0f}" cy="{H*0.24:.0f}" r="{H*0.5:.0f}" fill="{ROUGE}" opacity="0.14"/>')
    if clair:
        d.append(masque(W * 0.86, H * 0.88, H * 0.80, 0.13, CUIVRE, simple=True))
        c['cream'] = CHARBON
    else:
        d.append(masque(W * 0.86, H * 0.88, H * 0.80, 0.11, CREME, simple=True))
    d.append(MOTIFS[motif](c, min(W, H), W * 0.5, H * 0.45))
    d.append('</svg>')
    return ''.join(d)


# --------------------------------------------------------------------------
# Catalogue de référence (16 visuels)
# --------------------------------------------------------------------------
CATALOGUE = [
    # slug, titre, catégorie, motif, ton
    ('shooting-mariage-eau',      'Reportage photo et vidéo — Mariage à ciel ouvert', 'photo', 'photo', 'sombre'),
    ('shooting-corporate',        'Shooting corporate — Portraits et locaux', 'photo', 'photo', 'chaleureux'),
    ('shooting-produits',         'Photographie produit — Catalogue e-commerce', 'photo', 'photo', 'sombre'),
    ('shooting-portrait-equipe',  "Portrait d'équipe — 15 personnes en studio", 'photo', 'photo', 'chaleureux'),
    ('video-corporate',           'Film corporate — Institutionnel 90 secondes', 'video', 'evenement', 'chaleureux'),
    ('video-mariage',             'Vidéo de mariage — Drone et rushes du jour', 'video', 'evenement', 'sombre'),
    ('video-drone',               'Prise de vue aérienne — Sites et événementiel', 'video', 'evenement', 'chaleureux'),
    ('identite-visuelle',         'Identité visuelle — Logo, charte et couleurs', 'design', 'design', 'chaleureux'),
    ('design-brochure',           'Design de brochure — Rapport annuel 32 pages', 'design', 'design', 'sombre'),
    ('packaging-produit',         'Packaging — Étiquette et sachet pour jus de bissap', 'design', 'design', 'chaleureux'),
    ('banniere-publitaire',       'Bannière publicitaire — 4 × 2 m sur bâche', 'impression', 'impression', 'chaleureux'),
    ('flyers-campagne',           'Flyers de campagne — Série de 6 formats', 'impression', 'impression', 'sombre'),
    ('cartes-visite',             'Cartes de visite — Papier 350 g gaufré or', 'impression', 'impression', 'chaleureux'),
    ('stickers-vitrine',          'Stickers vitrine — Vinyle cruiser 10 × 15 cm', 'impression', 'impression', 'sombre'),
    ('kakemono-evenement',        'Kakémono roll-up — Stand 80 × 200 cm', 'impression', 'impression', 'sombre'),
    ('site-vitrine',              'Site vitrine — 6 pages responsive sur mesure', 'web', 'web', 'sombre'),
    ('boutique-en-ligne',         'Boutique en ligne — Catalogue et paiement mobile', 'web', 'web', 'chaleureux'),
    ('reseaux-sociaux',           'Réseaux sociaux — Calendrier éditorial 30 jours', 'web', 'web', 'sombre'),
    ('referencement-seo',         'Référencement SEO — Audit et suivi de position', 'web', 'web', 'chaleureux'),
]

CATEGORIES = [
    ('photo',       'Photo & Vidéo',       'photo',       'sombre'),
    ('design',      'Design & Identité',   'design',      'clair'),
    ('impression',  'Impression & Supports','impression', 'chaleureux'),
    ('web',         'Web & Digital',      'web',         'sombre'),
    ('evenement',   'Événements',          'evenement',   'chaleureux'),
    ('photo',       'Mariage',             'photo',       'clair'),
    ('design',      'Packaging',           'design',      'sombre'),
    ('impression',  'Signalétique',        'impression', 'sombre'),
]

BANNIERES = [
    ('b1', 'Imagerie, design et digital au Burkina Faso',
     'Studio intégré à Ouagadougou — de la prise de vue au site en ligne.', ROUGE),
    ('b2', 'Votre marque mérite mieux qu\'un catalogue PDF',
     'Identité visuelle, supports imprimés et patrimoine numérique.', CUIVRE),
    ('b3', 'Shooting corporate en 48 heures',
     'Locaux, équipes, produits : livrables prêts pour vos supports.', '#8E2A20'),
    ('b4', 'Livraison partout au Burkina Faso',
     'Supports physiques et numériques, de Ouaga à Bobo-Dioulasso.', OR),
]


def main():
    n = 0
    for slug, titre, cat, motif, tone in CATALOGUE:
        svg = visuel_catalogue(slug, titre, cat, motif, tone)
        open(os.path.join(ROOT, f'cat-{slug}.svg'), 'w', encoding='utf-8').write(svg)
        n += 1
    for i, (slug, titre, motif, tone) in enumerate(CATEGORIES):
        svg = visuel_categorie(f'c{i}', titre, motif, tone)
        open(os.path.join(ROOT, f'cat-categorie-{i+1}.svg'), 'w', encoding='utf-8').write(svg)
        n += 1
    for slug, titre, st, accent in BANNIERES:
        svg = visuel_banniere(slug, titre, st, accent)
        open(os.path.join(ROOT, f'banniere-{slug}.svg'), 'w', encoding='utf-8').write(svg)
        n += 1
    # vignette « à propos » (buste de marque)
    svg = visuel_banniere('marque', 'Notre signature', 'Le masque de bronze', CUIVRE, size=(1200, 900))
    open(os.path.join(ROOT, 'signature-rood-wooko.svg'), 'w', encoding='utf-8').write(svg)
    n += 1
    print(f'{n} visuels SVG générés dans {ROOT}')
    tot = sum(os.path.getsize(os.path.join(ROOT, f)) for f in os.listdir(ROOT))
    print(f'poids total : {tot/1024:.0f} Ko')


if __name__ == '__main__':
    main()
