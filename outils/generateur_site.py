#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Générateur des pages du site ROOD-WOOKO DIGITAL.
Produit index.html, catalogue.html et contact.html à partir d'une source unique,
ce qui garantit un en-tête, un pied de page et une charte rigoureusement
identiques sur les trois pages.
"""
import os

SITE = '/workspace/rood-wooko-digital'

# ---------------------------------------------------------------- CHARTE / DONNÉES
NOM      = 'ROOD-WOOKO DIGITAL'
VILLE    = 'BURKINA FASO, OUAGADOUGOU'
TEL      = '+226 78 45 04 46'
TEL_HREF = 'tel:+22678450446'
WA       = '+226 56 43 31 22'
WA_HREF  = 'https://wa.me/22656433122'
ADRESSE  = 'Rue 9.19, Porte 180'

# URL sociales à remplacer par le propriétaire (voir js/main.js, constante RWD_LINKS)
URL_FACEBOOK  = 'https://www.facebook.com/VOTRE-PAGE-FACEBOOK'
URL_TIKTOK    = 'https://www.tiktok.com/@VOTRE-COMPTE-TIKTOK'
URL_GALERIE   = 'GALERIE_SERVEUR_URL'
URL_INSTAGRAM = 'https://www.instagram.com/VOTRE-COMPTE-INSTAGRAM'

CATEGORIES = [
    ('photo',      'Photo'),
    ('video',      'Vidéo'),
    ('design',     'Design'),
    ('impression', 'Impression'),
    ('web',        'Web'),
]

# --------------------------------------------------------------------- ICÔNES
def svg(paths, vb='0 0 24 24', extra=''):
    return (f'<svg viewBox="{vb}" aria-hidden="true" focusable="false"{extra}>'
            f'{paths}</svg>')

I = {
 'livre':  svg('<path fill="currentColor" d="M3 3h13v13H3zM16 8h5v12H8v-5"/>'),
 'tel':    svg('<path fill="currentColor" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.58 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.46.57 3.6a1 1 0 0 1-.25 1z"/>'),
 'whatsapp': svg('<path fill="currentColor" d="M17.47 14.38c-.3-.15-1.75-.86-2.02-.96-.27-.1-.47-.15-.67.15-.2.3-.77.96-.94 1.16-.17.2-.35.22-.64.08-.3-.15-1.25-.46-2.38-1.47-.88-.78-1.47-1.75-1.65-2.05-.17-.3-.02-.46.13-.6.13-.13.3-.35.44-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.6-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.22 3.08c.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.69.63.71.22 1.36.19 1.87.12.57-.09 1.75-.72 2-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35zM12.04 21.5h-.01c-1.75 0-3.47-.47-4.98-1.36l-.36-.21-3.7.97.99-3.61-.23-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.89 9.9-9.89 2.64 0 5.13 1.03 7 2.9a9.83 9.83 0 0 1 2.89 7c0 5.45-4.44 9.89-9.9 9.89z M20.52 3.45A11.8 11.8 0 0 0 12.04 0C5.46 0 .08 5.38.08 11.96c0 2.1.55 4.16 1.6 5.97L0 24l6.2-1.63a11.9 11.9 0 0 0 5.84 1.48h.01c6.58 0 11.94-5.38 11.94-11.96 0-3.2-1.25-6.2-3.47-8.45z"/>'),
 'pin':    svg('<path fill="currentColor" d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/>'),
 'mail':   svg('<path fill="currentColor" d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1zm9 8L4.2 7H19.8L12 13z"/>'),
 'horloge':svg('<path fill="currentColor" d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm1 5h-2v6l5 3 1-1.7-4-2.3V7z"/>'),
 'recherche': svg('<path fill="currentColor" d="M15.5 14h-.79l-.28-.27a6.5 6.5 0 1 0-.7.7l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0A4.5 4.5 0 1 1 14 9.5 4.5 4.5 0 0 1 9.5 14z"/>'),
 'panier': svg('<path fill="currentColor" d="M7 18a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm10 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4zM1 2h3.3l.6 2h15.8c.9 0 1.6.8 1.5 1.7l-1.7 8.1c-.1.7-.7 1.2-1.4 1.2H6.2c-.7 0-1.3-.5-1.5-1.2L2.4 5H1V2z"/>'),
 'compte': svg('<path fill="currentColor" d="M12 12a5 5 0 1 0 0-10 5 5 0 0 0 0 10zm0 2c-4.4 0-8 2.2-8 5v3h16v-3c0-2.8-3.6-5-8-5z"/>'),
 'menu':   svg('<path fill="currentColor" d="M3 6h18v2H3V6zm0 5h18v2H3v-2zm0 5h18v2H3v-2z"/>'),
 'fermer': svg('<path fill="currentColor" d="M18.3 5.7 12 12l6.3 6.3-1.4 1.4L10.6 13.4 4.3 19.7 2.9 18.3 9.2 12 2.9 5.7 4.3 4.3l6.3 6.3 6.3-6.3z"/>'),
 'chevron':svg('<path fill="currentColor" d="M7.4 8.6 12 13.2l4.6-4.6L18 10l-6 6-6-6z"/>'),
 'gauche': svg('<path fill="currentColor" d="M15.4 7.4 14 6l-6 6 6 6 1.4-1.4L10.8 12z"/>'),
 'droite': svg('<path fill="currentColor" d="M8.6 16.6 10 18l6-6-6-6-1.4 1.4 4.6 4.6z"/>'),
 'fleche': svg('<path fill="currentColor" d="M12 4l-1.4 1.4 5.6 5.6H4v2h12.2l-5.6 5.6L12 20l8-8z"/>'),
 'etoile': svg('<path fill="currentColor" d="m12 17.3-6.2 3.7 1.6-7L2 9.2l7.1-.6L12 2l2.9 6.6 7.1.6-5.4 4.8 1.6 7z"/>'),
 'galerie':svg('<path fill="currentColor" d="M21 19V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2zM8.5 13.5l2.5 3 3.5-4.5 4.5 6H5l3.5-4.5z"/>'),
 'facebook': svg('<path fill="currentColor" d="M22 12.06C22 6.5 17.52 2 12 2S2 6.5 2 12.06c0 5 3.66 9.15 8.44 9.94v-7.03H7.9v-2.91h2.54V9.85c0-2.52 1.49-3.91 3.77-3.91 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.78-1.63 1.57v1.89h2.78l-.44 2.91h-2.34V22c4.78-.79 8.44-4.94 8.44-9.94z"/>'),
 'tiktok': svg('<path fill="currentColor" d="M16.6 5.82A4.28 4.28 0 0 1 15.54 3h-3.09v12.4a2.59 2.59 0 0 1-2.59 2.5 2.59 2.59 0 0 1 0-5.18c.27 0 .52.04.76.12v-3.2a5.87 5.87 0 0 0-.76-.05A5.72 5.72 0 0 0 4.14 15.3 5.72 5.72 0 0 0 9.86 21a5.72 5.72 0 0 0 5.72-5.72V9.01a7.35 7.35 0 0 0 4.28 1.38V7.3a4.29 4.29 0 0 1-3.26-1.48z"/>'),
 'instagram': svg('<path fill="currentColor" d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41-.56-.22-.96-.48-1.38-.9-.42-.42-.68-.82-.9-1.38-.16-.42-.36-1.06-.41-2.23-.06-1.27-.07-1.65-.07-4.85s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41 1.27-.06 1.65-.07 4.85-.07m0 2.12c-3.15 0-3.5.01-4.74.07-1.14.05-1.76.24-2.17.4-.55.21-.94.47-1.35.88-.41.41-.67.8-.88 1.35-.16.41-.35 1.03-.4 2.17-.06 1.24-.07 1.59-.07 4.74s.01 3.5.07 4.74c.05 1.14.24 1.76.4 2.17.21.55.47.94.88 1.35.41.41.8.67 1.35.88.41.16 1.03.35 2.17.4 1.24.06 1.59.07 4.74.07s3.5-.01 4.74-.07c1.14-.05 1.76-.24 2.17-.4.55-.21.94-.47 1.35-.88.41-.41.67-.8.88-1.35.16-.41.35-1.03.4-2.17.06-1.24.07-1.59.07-4.74s-.01-3.5-.07-4.74c-.05-1.14-.24-1.76-.4-2.17a3.6 3.6 0 0 0-.88-1.35 3.6 3.6 0 0 0-1.35-.88c-.41-.16-1.03-.35-2.17-.4-1.24-.06-1.59-.07-4.74-.07zM12 7.38a4.62 4.62 0 1 1 0 9.24 4.62 4.62 0 0 1 0-9.24zm0 7.62a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM18.54 6.78a1.08 1.08 0 1 1-2.15 0 1.08 1.08 0 0 1 2.15 0z"/>'),
}

# ------------------------------------------------------------------ CATALOGUE
# (slug, nom, catégorie, prix FCFA, description, avis, populaire, mots-clés, image)
CATALOGUE = [
 ('shooting-mariage-eau', 'Reportage photo et vidéo — Mariage à ciel ouvert', 'photo', 280000,
  "Journée complète : préparation, cérémonie à l'extérieur, portraits de famille et teaser vertical pour les réseaux.",
  48, 95, 'mariage photo video reportage couple ceremony', 'cat-shooting-mariage-eau.svg'),
 ('shooting-corporate', 'Shooting corporate — Portraits et locaux', 'photo', 180000,
  "Session d'une demi-journée : 20 portraits, produits, locaux, mise en scène aux couleurs de votre marque.",
  26, 88, 'corporate portrait locaux entreprise photo', 'cat-shooting-corporate.svg'),
 ('shooting-produits', 'Photographie produit — Catalogue e-commerce', 'photo', 65000,
  "Série de 30 visuels produits sur fond blanc ou neutre, livrés en haute définition et optimisés pour la boutique.",
  19, 72, 'produit e-commerce catalogue photo fond blanc', 'cat-shooting-produits.svg'),
 ('shooting-portrait-equipe', "Portrait d'équipe — 15 personnes en studio", 'photo', 95000,
  "Mise en lumière du collectif, cadrage horizontal pour la page équipe et format carré pour les réseaux sociaux.",
  11, 61, 'equipe portrait studio groupe entreprise', 'cat-shooting-portrait-equipe.svg'),
 ('video-corporate', 'Film corporate — Institutionnel 90 secondes', 'video', 350000,
  "Conception, tournage et montage d'un film de 90 secondes : interviews, plans produits et voix off.",
  33, 90, 'video film corporate institutionnel montage', 'cat-video-corporate.svg'),
 ('video-mariage', 'Vidéo de mariage — Drone et rushes du jour', 'video', 300000,
  "Deux caméraurs, drone réglementé, rushes du jour et film de 6 minutes.",
  22, 84, 'video mariage drone rush film', 'cat-video-mariage.svg'),
 ('video-drone', 'Prise de vue aérienne — Sites et événementiel', 'video', 200000,
  "Survol de site, de parcelle ou de chantier, avec plans verticaux pour les réseaux et plans larges pour la vidéo.",
  9, 54, 'drone aerien site parcelle immobilier video', 'cat-video-drone.svg'),
 ('identite-visuelle', 'Identité visuelle — Logo, charte et couleurs', 'design', 150000,
  "Construction du logotype, déclinaisons monochrome et couleur, palette de couleurs et mini charte graphique de 6 pages.",
  14, 92, 'logo identite charte graphique design couleur', 'cat-identite-visuelle.svg'),
 ('design-brochure', 'Design de brochure — Rapport annuel 32 pages', 'design', 120000,
  "Maquette, mise en page et suivi d'impression d'une brochure de 32 pages, en français, prête pour le papier.",
  8, 58, 'brochure rapport annuel mise en page design', 'cat-design-brochure.svg'),
 ('packaging-produit', 'Packaging — Étiquette et sachet pour jus de bissap', 'design', 95000,
  "Étiquette et sachet pour un jus local : arborescence, zones d'impression, choix du papier et prepostes.",
  6, 47, 'packaging etiqueta sachet produit bissap jus', 'cat-packaging-produit.svg'),
 ('banniere-publitaire', 'Bannière publicitaire — 4 × 2 m sur bâche', 'impression', 45000,
  "Bâche 440 g/m² avec ourlets et œillets renforcés, resistante au soleil, pose sur échafaudage ou clôture.",
  17, 79, 'banniere advertise bâche grand format evenement', 'cat-banniere-publitaire.svg'),
 ('flyers-campagne', 'Flyers de campagne — Série de 6 formats', 'impression', 35000,
  "Six formats (A6, A5, A4, DL, 10 × 15, 10 × 21) imprimés sur couché 135 g ou 170 g, recto-verso.",
  21, 70, 'flyers campagne tract affiche format impression', 'cat-flyers-campagne.svg'),
 ('cartes-visite', 'Cartes de visite — Papier 350 g gaufré or', 'impression', 25000,
  "Cartes 85 × 55 mm sur 350 g avec pelliculage mat, dorure à chaud et coins arrondis, fichier prêt à l'emploi.",
  29, 86, 'carte visite papier dorure gaufrage', 'cat-cartes-visite.svg'),
 ('stickers-vitrine', 'Stickers vitrine — Vinyle cruiser 10 × 15 cm', 'impression', 15000,
  "Vinyle cruiser adhésif, découpe à la forme, usage intérieur ou extérieur, pose sans trace de colle.",
  12, 52, 'sticker vitrine vinyle autocollant adhesif', 'cat-stickers-vitrine.svg'),
 ('kakemono-evenement', 'Kakémono roll-up — Stand 80 × 200 cm', 'impression', 55000,
  "Roll-up aluminium 80 × 200 cm avec housse, visuel imprimé en 1440 dpi et montage en trois minutes.",
  10, 66, 'kakemono roll-up stand salon expo', 'cat-kakemono-evenement.svg'),
 ('site-vitrine', 'Site vitrine — 6 pages responsive sur mesure', 'web', 450000,
  "Site statique rapide, 6 pages, formulaires, galerie serveur et mise en ligne avec nom de domaine.",
  31, 93, 'site vitrine web responsive pages', 'cat-site-vitrine.svg'),
 ('boutique-en-ligne', 'Boutique en ligne — Catalogue et paiement mobile', 'web', 750000,
  "Boutique avec catalogue filtrable, panier, paiement Mobile Money et livraison National Burkina Faso.",
  24, 89, 'boutique en ligne e-commerce panier paiement', 'cat-boutique-en-ligne.svg'),
 ('reseaux-sociaux', 'Réseaux sociaux — Calendrier éditorial 30 jours', 'web', 180000,
  "Trente jours de publications, visuels et textes, programmés pour Facebook, Instagram et TikTok.",
  16, 74, 'reseaux sociaux contenu calendrier editorial', 'cat-reseaux-sociaux.svg'),
 ('referencement-seo', 'Référencement SEO — Audit et suivi de position', 'web', 200000,
  "Audit technique, optimisation des pages, stratégie de mots-clés et suivi mensuel des positions.",
  7, 57, 'seo referencement audit mots cles position', 'cat-referencement-seo.svg'),
]

# ------------------------------------------------------------------- UTILITAIRES
def esc(t):
    return (str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;'))

def prix_fr(p):
    return '{:,}'.format(p).replace(',', ' ')

def socials(reseau, libelle, href):
    return (f'<a class="social-bouton" data-reseau="{reseau}" href="{esc(href)}" '
            f'target="_blank" rel="noopener" title="{esc(libelle)}" '
            f'aria-label="{esc(libelle)} — ROOD-WOOKO DIGITAL (nouvel onglet)">'
            f'{I[reseau] if reseau in I else ""}</a>')

def rangee_socials():
    return ('<div class="socials">'
            + socials('facebook', 'Facebook', URL_FACEBOOK)
            + socials('tiktok', 'TikTok', URL_TIKTOK)
            + socials('galerie', 'Galerie de serveur', URL_GALERIE)
            + socials('whatsapp', 'WhatsApp', WA_HREF)
            + socials('instagram', 'Instagram', URL_INSTAGRAM)
            + '</div>')

# =============================================================== EN-TÊTE COMMUN
def bloc_topbar():
    return f'''
  <div class="topbar">
    <div class="topbar-inner">
      <p class="topbar-livraison">{I['livre']}<span>Livraison partout au Burkina Faso</span></p>
      <div class="topbar-contact">
        <span class="topbar-lieu">{VILLE}</span>
        <a href="{TEL_HREF}" aria-label="Appeler le {TEL}">{I['tel']}{TEL}</a>
        <a href="{WA_HREF}" target="_blank" rel="noopener" aria-label="Écrire sur WhatsApp au {WA}">{I['whatsapp']}{WA}</a>
      </div>
    </div>
  </div>'''

def bloc_entete(page):
    options = ''.join(
        f'<option value="{c}">{n}</option>' for c, n in CATEGORIES)
    return f'''
  <div class="entete-inner">
    <a class="marque" href="index.html" aria-label="{NOM} — retour à l'accueil">
      <picture>
        <source media="(prefers-reduced-motion: reduce)" srcset="assets/logo/header-static.png">
        <img class="marque-logo" src="assets/logo/header.gif" width="300" height="89"
             alt="Logo animé {NOM} : le logotype cuivré et les têtes de la marque en émergeant" loading="eager">
      </picture>
      <span class="marque-signature" aria-hidden="true">
        <span class="marque-signature-titre">Studio créatif</span>
        <span class="marque-signature-ville">Ouagadougou, Burkina Faso</span>
      </span>
    </a>

    <form class="recherche" id="form-recherche" role="search" action="catalogue.html" method="get">
      <label class="visuellement-cache" for="recherche-categorie">Choisir une catégorie</label>
      <select class="recherche-select" id="recherche-categorie" name="cat">
        <option value="toutes">Toutes les catégories</option>
        {options}
      </select>
      <label class="visuellement-cache" for="recherche-champ">Rechercher un service ou un support</label>
      <input class="recherche-champ" id="recherche-champ" name="q" type="search"
             placeholder="Rechercher : shooting, bannière, logo…" autocomplete="off">
      <button class="recherche-btn" type="submit" aria-label="Lancer la recherche">{I['recherche']}<span>Rechercher</span></button>
    </form>

    <div class="outils">
      <button class="outil" type="button" aria-label="Mon compte">
        {I['compte']}<span>Compte</span>
        <span class="outil-compteur" data-compteur-compte>0</span>
      </button>
      <button class="outil" type="button" aria-label="Panier, aucun article">
        {I['panier']}<span>Panier</span>
        <span class="outil-compteur" data-compteur-panier>0</span>
      </button>
      <button class="bouton-menu" id="bouton-menu" type="button"
              aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="ceinture-nav">
        {I['menu']}
      </button>
    </div>
  </div>'''

def bloc_ceinture(page):
    liens = [('index.html', 'Accueil'), ('catalogue.html', 'Catalogue'), ('contact.html', 'Contact')]
    items = ''.join(
        f'<a class="nav-lien" data-page="{href}" href="{href}">{txt}</a>' for href, txt in liens)
    menu = ''.join(
        f'<a href="catalogue.html?cat={c}"><span class="puce"></span>{n}'
        f'<span class="compte"></span></a>' for c, n in CATEGORIES)
    return f'''
  <div class="ceinture-inner">
    <div class="nav-categories" id="nav-categories" data-ouvert="false">
      <button type="button" aria-expanded="false" aria-controls="menu-categories">
        {I['menu']} Toutes les catégories {I['chevron']}
      </button>
      <div class="menu-categories" id="menu-categories">{menu}</div>
    </div>
    {items}
    <button class="bouton-menu" type="button" data-fermer-menu aria-label="Fermer le menu">{I['fermer']}</button>
  </div>'''

# =============================================================== PIED DE PAGE
def bloc_pied():
    cats = ''.join(
        f'<li><a href="catalogue.html?cat={c}">{n}</a></li>' for c, n in CATEGORIES)
    rapides = ''.join([
        '<li><a href="index.html">Accueil</a></li>',
        '<li><a href="catalogue.html">Catalogue complet</a></li>',
        '<li><a href="catalogue.html?cat=photo">Photographie</a></li>',
        '<li><a href="catalogue.html?cat=design">Identité visuelle</a></li>',
        '<li><a href="catalogue.html?cat=impression">Impression</a></li>',
        '<li><a href="catalogue.html?cat=web">Sites et e-commerce</a></li>',
        '<li><a href="contact.html">Contact et plan d\'accès</a></li>',
    ])
    return f'''
  <div class="conteneur">
    <div class="pied-grille">
      <div>
        <div class="pied-marque">
          <picture>
            <source media="(prefers-reduced-motion: reduce)" srcset="assets/logo/header-static.png">
            <img class="pied-logo" src="assets/logo/header.gif" width="300" height="89"
                 alt="Logo {NOM} — {VILLE}" loading="lazy">
          </picture>
        </div>
        <p>{NOM} est un studio créatif basé à {VILLE}. Nous produisons l'imagerie,
           l'identité visuelle, les supports imprimés et les sites web des entreprises
           et des institutions du Burkina Faso.</p>
        <div class="pied-socials">
          {socials('facebook', 'Facebook', URL_FACEBOOK)}
          {socials('tiktok', 'TikTok', URL_TIKTOK)}
          {socials('galerie', 'Galerie de serveur', URL_GALERIE)}
          {socials('whatsapp', 'WhatsApp', WA_HREF)}
          {socials('instagram', 'Instagram', URL_INSTAGRAM)}
        </div>
      </div>

      <div>
        <h3>Catégories</h3>
        <ul class="pied-liens">{cats}</ul>
      </div>

      <div>
        <h3>Contact</h3>
        <ul class="pied-contact">
          <li>{I['pin']}<span>{ADRESSE}<br>{VILLE}<br>Burkina Faso</span></li>
          <li>{I['tel']}<a href="{TEL_HREF}">{TEL}</a></li>
          <li>{I['whatsapp']}<a href="{WA_HREF}" target="_blank" rel="noopener">{WA}</a></li>
          <li>{I['horloge']}<span>Lun – Sam : 8 h – 18 h<br>Dimanche : sur rendez-vous</span></li>
        </ul>
      </div>

      <div>
        <h3>Liens rapides</h3>
        <ul class="pied-liens">{rapides}</ul>
      </div>
    </div>

    <div class="pied-copyright">
      <span>© <span data-annee>2026</span> {NOM} — Tous droits réservés</span>
      <span>Studio photo, design et développement web — {VILLE}</span>
    </div>
  </div>'''

def bloc_wa():
    return f'''
  <a class="wa-flottant" href="{WA_HREF}" target="_blank" rel="noopener"
     aria-label="Contacter {NOM} sur WhatsApp au {WA}">{I['whatsapp']}</a>'''

# ================================================================ CARTES
def carte_produit(item, compact=False):
    slug, nom, cat, prix, desc, avis, pop, mots, img = item
    note = min(5, round(3.4 + pop / 48.0, 1))
    etoiles = I['etoile'] * 5
    return f'''
      <article class="carte-produit" data-categorie="{cat}" data-prix="{prix}"
               data-nom="{esc(nom)}" data-mots="{esc(mots)}" data-description="{esc(desc)}"
               data-populaire="{pop}">
        <div class="carte-produit-media">
          <a class="carte-produit-img" href="catalogue.html?cat={cat}"
             aria-label="Voir {esc(nom)} dans le catalogue">
            <img src="assets/img/{img}" width="800" height="600" loading="lazy"
                 alt="{esc(nom)} — aperçu du service {nom.split('—')[0].strip()} proposé par {NOM}">
          </a>
          {rangee_socials()}
        </div>
        <div class="carte-produit-corps">
          <span class="carte-produit-cat">{esc(dict(CATEGORIES)[cat])}</span>
          <h3>{esc(nom)}</h3>
          <p class="desc">{esc(desc)}</p>
          <div class="etoiles" aria-label="Note : {note} sur 5, {avis} avis">{etoiles}<span class="avis">({note} · {avis} avis)</span></div>
          <div class="carte-produit-pied">
            <p class="prix"><span class="prix-prefixe">À partir de</span>{prix_fr(prix)} <small>FCFA</small></p>
          </div>
        </div>
      </article>'''

def carte_categorie(index, titre, sous_titre, cat, img):
    return f'''
        <a class="carte-cat" href="catalogue.html?cat={cat}">
          <img src="assets/img/{img}" width="520" height="360" loading="lazy"
               alt="Catégorie {esc(titre)} — {esc(sous_titre)}">
          <span class="carte-cat-corps">
            <span>
              <h3>{esc(titre)}</h3>
              <p>{esc(sous_titre)}</p>
            </span>
            <span class="fleche-lien" aria-hidden="true">{I['fleche']}</span>
          </span>
        </a>'''

CATEGORIES_VISUELLES = [
    (1, 'Photo', 'Shooting, reportage et catalogue produit', 'photo'),
    (2, 'Design &amp; Identité', 'Logo, charte, brochure et packaging', 'design'),
    (3, 'Impression &amp; Supports', 'Bannières, flyers, cartes et kakémonos', 'impression'),
    (4, 'Web &amp; Digital', 'Sites vitrines, boutiques et référencement', 'web'),
    (5, 'Film &amp; Vidéo', 'Institutionnel, mariage et prise de vue aérienne', 'video'),
    (6, 'Mariage', 'Reportage photo et vidéo du jour J', 'photo'),
    (7, 'Packaging', 'Étiquettes et sachets pour produits locaux', 'design'),
    (8, 'Signalétique', 'Kakémonos, vitrines et signalétique d\'entreprise', 'impression'),
]

# ================================================================== PAGE ACCUEIL
def page_accueil():
    slides = [
        ('banniere-b1.svg', 'Studio créatif à Ouagadougou',
         'Imagerie, design et digital au service de votre marque',
         "Photographie, identité visuelle, impression et sites web : nous produisons, "
         "nous imprimons et nous livrons partout au Burkina Faso."),
        ('banniere-b2.svg', 'Vos supports,ouvrés à l\'heure',
         'Votre marque mérite mieux qu\'un catalogue PDF',
         "De l'idée au fichier d'impression : charte graphique, supports physiques "
         "et patrimoine numérique restent cohérents entre eux."),
        ('banniere-b3.svg', 'Shooting corporate en 48 heures',
         'Des images nettes, exploitables tout de suite',
         "Locaux, équipes, produits : nous venons au studio avec le matériel, "
         "vous repartez avec des visuels prêts à publier."),
        ('banniere-b4.svg', 'Livraison partout au Burkina Faso',
         'Votre site vitrine prêt en quinze jours',
         "Un site rapide, responsive et administrable sans code, avec un formulaire "
         "de contact relié à WhatsApp."),
    ]
    diapo = ''.join(
        f'''<div class="heros-slide" role="group" aria-roledescription="diapositive"
             aria-label="Diapositive {i+1} sur {len(slides)}" aria-hidden="true">
              <img src="assets/img/{img}" width="1920" height="640" alt="{esc(titre)}">
              <div class="heros-contenu"><div class="heros-texte">
                <span class="sur-titre">{esc(surtitre)}</span>
                <h2>{esc(titre)}</h2>
                <p>{esc(para)}</p>
                <div class="heros-actions">
                  <a class="btn btn-or" href="catalogue.html">Découvrir le catalogue</a>
                  <a class="btn btn-fantome-clair" href="contact.html">Nous contacter</a>
                </div>
              </div></div>
            </div>''' for i, (img, surtitre, titre, para) in enumerate(slides))

    points = ''.join(
        f'<button class="heros-point" type="button" role="tab" aria-selected="{"true" if i==0 else "false"}" '
        f'aria-label="Aller à la diapositive {i+1}"></button>' for i in range(len(slides)))

    chats = ''.join(
        carte_categorie(idx, t, st, cat, f'cat-categorie-{idx}.svg')
        for idx, t, st, cat in CATEGORIES_VISUELLES)

    rail1 = ''.join(carte_produit(i) for i in CATALOGUE if i[2] in ('photo', 'video'))
    rail2 = ''.join(carte_produit(i) for i in CATALOGUE if i[2] in ('design', 'impression'))
    rail3 = ''.join(carte_produit(i) for i in CATALOGUE if i[2] == 'web')

    logos = [
        ('header', 'Logotype principal', False),
        ('hero',   'La tête traversant le logotype', True),
        ('buste',  'Le buste de la marque', True),
        ('dots',   'Les quatre points du masque', True),
        ('avatar', 'L\'emblème circulaire', True),
    ]
    bloc_logos = ''.join(
        f'''<figure class="logo-cadre{' logo-cadre--clair' if clair else ''}">
              <picture>
                <source media="(prefers-reduced-motion: reduce)" srcset="assets/logo/{n}-static.png">
                <img src="assets/logo/{n}.gif" width="300" height="89" loading="lazy"
                     alt="Proposition de logo animé {NOM} — {esc(cap)}">
              </picture>
              <figcaption>{esc(cap)}</figcaption>
            </figure>''' for n, cap, clair in logos)

    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{NOM} — Studio photo, design et web à Ouagadougou</title>
  <meta name="description" content="{NOM} à {VILLE} : photographie, vidéo, identité visuelle, impression et création de sites web. Livraison partout au Burkina Faso. Appelez le {TEL}.">
  <meta name="theme-color" content="#1A1A1A">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="css/style.css">
</head>
<body id="haut">
  <a class="lien-evitement" href="#contenu">Aller au contenu principal</a>

  <header class="entete">
    {bloc_topbar()}
    {bloc_entete('index')}
  </header>

  <nav class="ceinture" id="ceinture-nav" aria-label="Navigation principale">
    {bloc_ceinture('index')}
  </nav>

  <main id="contenu">

    <section class="heros" id="heros" aria-roledescription="carrousel" aria-label="Nos services en bref">
      <div class="heros-piste">{diapo}</div>
      <button class="heros-fleche prev" type="button" aria-label="Diapositive précédente">{I['gauche']}</button>
      <button class="heros-fleche next" type="button" aria-label="Diapositive suivante">{I['droite']}</button>
      <div class="heros-points" role="tablist" aria-label="Choisir une diapositive">{points}</div>
      <figure class="heros-carte-logo">
        <picture>
          <source media="(prefers-reduced-motion: reduce)" srcset="assets/logo/hero-static.png">
          <img src="assets/logo/hero.gif" width="440" height="248" alt="Logo animé {NOM} — la tête de marque traverse le logotype">
        </picture>
        <figcaption>Notre signature animée</figcaption>
      </figure>
    </section>

    <section class="section" aria-labelledby="titre-expertises">
      <div class="conteneur">
        <div class="section-titre">
          <div>
            <span class="sur-titre">Nos expertises</span>
            <h2 id="titre-expertises">Tout ce qu'un studio doit savoir faire</h2>
            <p>De la prise de vue à la mise en ligne : une chaîne complète, pilotée sur place.</p>
          </div>
          <a class="lien-section" href="catalogue.html">Voir le catalogue complet →</a>
        </div>
        <div class="grille-cats">{chats}</div>
      </div>
    </section>

    <section class="section-serree" aria-labelledby="titre-photo">
      <div class="conteneur">
        <div class="section-titre">
          <div>
            <span class="sur-titre">Photographie &amp; vidéo</span>
            <h2 id="titre-photo">Des images qui font vendre</h2>
          </div>
          <a class="lien-section" href="catalogue.html?cat=photo">Toutes les prestations photo →</a>
        </div>
        <div class="rail" data-rail>
          <button class="rail-btn prev" type="button" aria-label="Faire défiler vers la gauche">{I['gauche']}</button>
          <div class="rail-piste">{rail1}</div>
          <button class="rail-btn next" type="button" aria-label="Faire défiler vers la droite">{I['droite']}</button>
        </div>
      </div>
    </section>

    <section class="section-serree" aria-labelledby="titre-design">
      <div class="conteneur">
        <div class="section-titre">
          <div>
            <span class="sur-titre">Design &amp; impression</span>
            <h2 id="titre-design">Une identité qui tient sur tous les supports</h2>
          </div>
          <a class="lien-section" href="catalogue.html?cat=impression">Tous les supports →</a>
        </div>
        <div class="rail" data-rail>
          <button class="rail-btn prev" type="button" aria-label="Faire défiler vers la gauche">{I['gauche']}</button>
          <div class="rail-piste">{rail2}</div>
          <button class="rail-btn next" type="button" aria-label="Faire défiler vers la droite">{I['droite']}</button>
        </div>
      </div>
    </section>

    <section class="section-serree" aria-labelledby="titre-web">
      <div class="conteneur">
        <div class="section-titre">
          <div>
            <span class="sur-titre">Web &amp; digital</span>
            <h2 id="titre-web">Votre vitrine sur internet, en français</h2>
          </div>
          <a class="lien-section" href="catalogue.html?cat=web">Tous les services web →</a>
        </div>
        <div class="rail" data-rail>
          <button class="rail-btn prev" type="button" aria-label="Faire défiler vers la gauche">{I['gauche']}</button>
          <div class="rail-piste">{rail3}</div>
          <button class="rail-btn next" type="button" aria-label="Faire défiler vers la droite">{I['droite']}</button>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="titre-marque">
      <div class="conteneur">
        <div class="section-titre">
          <div>
            <span class="sur-titre">La marque</span>
            <h2 id="titre-marque">Un logotype animé, en cuivre et en bronze</h2>
            <p>Les cinq propositions de logo animé retenues pour {NOM}, toutes construites
               autour du masque de bronze qui donne son visage à la marque.</p>
          </div>
        </div>
        <div class="bandeau-marque">
          <h3>Propositions de logo animé</h3>
          <div class="logos-animes">{bloc_logos}</div>
        </div>
      </div>
    </section>

    <section class="section-serree" aria-labelledby="titre-contact">
      <div class="conteneur">
        <div class="contact-rapide">
          <div class="bloc">
            <span class="icone">{I['tel']}</span>
            <div>
              <h3>Téléphone</h3>
              <a href="{TEL_HREF}">{TEL}</a><br>
              <span>Du lundi au samedi, 8 h – 18 h</span>
            </div>
          </div>
          <div class="bloc">
            <span class="icone">{I['whatsapp']}</span>
            <div>
              <h3>WhatsApp</h3>
              <a href="{WA_HREF}" target="_blank" rel="noopener">{WA}</a><br>
              <span>Devis rapide, envoi de visuels</span>
            </div>
          </div>
          <div class="bloc">
            <span class="icone">{I['pin']}</span>
            <div>
              <h3>Adresse</h3>
              <span>{ADRESSE}<br>{VILLE}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

  </main>

  <a class="retour-haut" href="#haut" data-retour-haut>▲ Retour en haut</a>

  <footer class="pied">
    {bloc_pied()}
  </footer>

  {bloc_wa()}
  <script src="js/main.js"></script>
</body>
</html>
'''

# ============================================================== PAGE CATALOGUE
def page_catalogue():
    puces = ''.join(
        f'<button class="puce-filtre" type="button" data-filtre="{c}" aria-pressed="false">{n}</button>'
        for c, n in CATEGORIES)
    aside = ''.join(
        f'<a href="#grille-produits" data-filtre="{c}">{n} <span class="nombre"></span></a>'
        for c, n in CATEGORIES)
    cartes = ''.join(carte_produit(i) for i in CATALOGUE)

    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Catalogue — {NOM}, studio à Ouagadougou</title>
  <meta name="description" content="Catalogue {NOM} : photographie, vidéo, identité visuelle, impression et sites web. {len(CATALOGUE)} prestations à partir de {prix_fr(min(i[3] for i in CATALOGUE))} FCFA. {VILLE}. Téléphone {TEL}, WhatsApp {WA}.">
  <meta name="theme-color" content="#1A1A1A">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="css/style.css">
</head>
<body id="haut">
  <a class="lien-evitement" href="#contenu">Aller au contenu principal</a>

  <header class="entete">
    {bloc_topbar()}
    {bloc_entete('catalogue')}
  </header>

  <nav class="ceinture" id="ceinture-nav" aria-label="Navigation principale">
    {bloc_ceinture('catalogue')}
  </nav>

  <main id="contenu">
    <section class="bandeau-page">
      <div class="conteneur">
        <p class="fil">Accueil / Catalogue</p>
        <h1>Catalogue des prestations {NOM}</h1>
        <p>{len(CATALOGUE)} prestations photographiques, graphiques, imprimées et web.
           Chaque fiche est suivie des cinq liens de partage de la marque : Facebook,
           TikTok, galerie de serveur, WhatsApp et Instagram.</p>
      </div>
    </section>

    <section class="section">
      <div class="conteneur">
        <div class="filtres" id="filtres">
          <span class="intitule">Filtrer :</span>
          <button class="puce-filtre" type="button" data-filtre="toutes" aria-pressed="true">Toutes</button>
          {puces}
          <span class="resultats" id="compte-resultats"></span>
        </div>

        <p class="recherche-info" id="recherche-info" data-visible="false"
           style="display:none;background:#FFF7E0;border:1px solid #F1C40F;border-radius:8px;padding:10px 14px;margin-bottom:18px;font-size:.88rem"></p>

        <div class="ligne-catalogue">
          <aside class="aside-catalogue" id="aside-categories" aria-label="Catégories du catalogue">
            <h2>Catégories</h2>
            <a href="#grille-produits" data-filtre="toutes">Tout le catalogue <span class="nombre"></span></a>
            {aside}
            <div class="note">
              <p><strong>Devis sur mesure.</strong> Les tarifs affichés sont des prix de départ
                 pour une prestation standard. Un devis définitif est établi après échange
                 sur votre besoin.</p>
              <p><a href="{WA_HREF}" target="_blank" rel="noopener">Demander un devis sur WhatsApp →</a></p>
            </div>
          </aside>

          <div>
            <div style="display:flex;justify-content:flex-end;align-items:center;gap:10px;margin-bottom:16px;flex-wrap:wrap">
              <label for="tri-catalogue" style="font-size:.86rem;color:var(--texte-doux)">Trier par</label>
              <select id="tri-catalogue" style="padding:9px 12px;border:1px solid var(--bordure-forte);border-radius:8px;background:#fff">
                <option value="populaire">Nos coups de cœur</option>
                <option value="prix-asc">Prix croissant</option>
                <option value="prix-desc">Prix décroissant</option>
                <option value="nom">Ordre alphabétique</option>
              </select>
            </div>

            <div class="grille-produits" id="grille-produits">{cartes}</div>

            <div class="message-vide" id="message-vide" data-visible="false">
              <p><strong>Aucune prestation ne correspond à votre recherche.</strong></p>
              <p>Essayez un autre mot-clé ou <a href="catalogue.html">voir tout le catalogue</a>.
                 Notre équipe répond au {TEL} et sur WhatsApp au {WA}.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>

  <a class="retour-haut" href="#haut" data-retour-haut>▲ Retour en haut</a>

  <footer class="pied">
    {bloc_pied()}
  </footer>

  {bloc_wa()}
  <script src="js/main.js"></script>
  <script src="js/catalogue.js"></script>
</body>
</html>
'''

# ================================================================ PAGE CONTACT
def page_contact():
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Contact et accès — {NOM}, {VILLE}</title>
  <meta name="description" content="Contactez {NOM} : {ADRESSE}, {VILLE}. Téléphone {TEL}, WhatsApp {WA}. Horaires, plan d'accès et formulaire de contact.">
  <meta name="theme-color" content="#1A1A1A">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="css/style.css">
</head>
<body id="haut">
  <a class="lien-evitement" href="#contenu">Aller au contenu principal</a>

  <header class="entete">
    {bloc_topbar()}
    {bloc_entete('contact')}
  </header>

  <nav class="ceinture" id="ceinture-nav" aria-label="Navigation principale">
    {bloc_ceinture('contact')}
  </nav>

  <main id="contenu">
    <section class="bandeau-page">
      <div class="conteneur">
        <p class="fil">Accueil / Contact</p>
        <h1>Nous écrire, nous appeler, nous rendre visite</h1>
        <p>Le studio est ouvert du lundi au samedi. Pour un devis, une question technique
           ou un rendez-vous, le plus rapide reste WhatsApp.</p>
      </div>
    </section>

    <section class="section">
      <div class="conteneur">
        <div class="grille-contact">

          <div>
            <form class="formulaire" id="formulaire-contact" novalidate>
              <h2>Formulaire de contact</h2>
              <p>Les champs marqués d'un astérisque sont obligatoires. La validation se fait
                 entièrement dans votre navigateur ; l'envoi se fait par WhatsApp ou par messagerie.</p>

              <div class="champ-deux">
                <div class="champ" id="champ-nom">
                  <label for="nom">Nom et prénom <span class="oblig">*</span></label>
                  <input type="text" id="nom" name="nom" autocomplete="name" required>
                  <span class="champ-erreur">Merci d'indiquer votre nom.</span>
                </div>
                <div class="champ" id="champ-societe">
                  <label for="societe">Entreprise / organisation</label>
                  <input type="text" id="societe" name="societe" autocomplete="organization">
                  <span class="champ-erreur">Ce champ est facultatif.</span>
                </div>
              </div>

              <div class="champ-deux">
                <div class="champ" id="champ-email">
                  <label for="email">Adresse e-mail <span class="oblig">*</span></label>
                  <input type="email" id="email" name="email" autocomplete="email" required>
                  <span class="champ-erreur">Merci d'indiquer une adresse e-mail valide.</span>
                </div>
                <div class="champ" id="champ-telephone">
                  <label for="telephone">Téléphone <span class="oblig">*</span></label>
                  <input type="tel" id="telephone" name="telephone" autocomplete="tel" required
                         placeholder="+226 70 00 00 00">
                  <span class="champ-erreur">Merci d'indiquer un numéro de téléphone.</span>
                </div>
              </div>

              <div class="champ" id="champ-sujet">
                <label for="sujet">Objet de la demande <span class="oblig">*</span></label>
                <select id="sujet" name="sujet" required>
                  <option value="">— Choisir un objet —</option>
                  <option>Photographie / reportage</option>
                  <option>Film et vidéo</option>
                  <option>Identité visuelle / design</option>
                  <option>Impression et supports</option>
                  <option>Site web et e-commerce</option>
                  <option>Référencement et réseaux sociaux</option>
                  <option>Autre demande</option>
                </select>
                <span class="champ-erreur">Merci de choisir un objet.</span>
              </div>

              <div class="champ" id="champ-message">
                <label for="message">Votre message <span class="oblig">*</span></label>
                <textarea id="message" name="message" required
                          placeholder="Décrivez votre besoin : type de projet, format, quantité, délais…"></textarea>
                <span class="champ-erreur">Merci d'écrire quelques mots sur votre besoin.</span>
              </div>

              <div class="form-actions">
                <button class="btn btn-rouge" type="submit">Envoyer via WhatsApp</button>
                <button class="btn btn-fantome" type="button" id="envoi-email">Envoyer par e-mail</button>
              </div>

              <p class="message-ok" id="message-ok" data-visible="false"></p>
            </form>
          </div>
            <div class="carte-info" style="text-align:center;margin-top:22px">
              <picture style="display:inline-block;max-width:190px">
                <source media="(prefers-reduced-motion: reduce)" srcset="assets/logo/avatar-static.png">
                <img src="assets/logo/avatar.gif" width="260" height="275" loading="lazy"
                     alt="Emblème animé {NOM} : la tête de marque émergeant d'un cercle">
              </picture>
              <h3 style="margin-top:12px">La marque en mouvement</h3>
              <p style="font-size:.87rem;color:var(--texte-doux);margin:0">
                Nos cinq propositions de logo animé sont utilisées sur l'ensemble du site.
                Choisissez celle qui vous ressemble le plus, nous la finalisons dans la journée.</p>
            </div>

          <div style="display:flex;flex-direction:column;gap:22px">
            <div class="carte-info">
              <h3>Coordonnées</h3>
              <div class="info-ligne">
                <span class="icone">{I['pin']}</span>
                <div class="contenu">
                  <strong>Adresse du studio</strong>
                  <span>{ADRESSE}<br>{VILLE}<br>Burkina Faso</span>
                </div>
              </div>
              <div class="info-ligne">
                <span class="icone">{I['tel']}</span>
                <div class="contenu">
                  <strong>Téléphone</strong>
                  <a href="{TEL_HREF}">{TEL}</a>
                </div>
              </div>
              <div class="info-ligne">
                <span class="icone">{I['whatsapp']}</span>
                <div class="contenu">
                  <strong>WhatsApp</strong>
                  <a href="{WA_HREF}" target="_blank" rel="noopener">{WA}</a>
                </div>
              </div>
              <div class="info-ligne">
                <span class="icone">{I['mail']}</span>
                <div class="contenu">
                  <strong>Réseaux sociaux</strong>
                  <span>Facebook, TikTok et Instagram — liens dans le pied de page et sous chaque photo du catalogue.</span>
                </div>
              </div>
            </div>

            <div class="carte-info horaires">
              <h3>Horaires d'ouverture</h3>
              <table>
                <tbody>
                  <tr><td>Lundi – Vendredi</td><td>8 h 00 – 18 h 00</td></tr>
                  <tr><td>Samedi</td><td>9 h 00 – 14 h 00</td></tr>
                  <tr><td>Dimanche</td><td>Sur rendez-vous</td></tr>
                </tbody>
              </table>
            </div>

            <div class="plan-acces">
              <h3>Plan d'accès (textuel)</h3>
              <ol>
                <li>Depuis le centre-ville de Ouagadougou, rejoindre le <strong>secteur 9</strong> par
                    la avenue de la Nation puis la rue 9.19.</li>
                <li>Repérer le <strong>n° 180</strong> : la porte du studio se situe juste après
                    une borne de recharge pour téléphone.</li>
                <li>Un <strong>portail bleu</strong> marque l'entrée de la cour ; la signalétique
                    ROOD-WOOKO DIGITAL est fixée sur la porte.</li>
                <li>Deux places de stationnement sont disponibles devant la porte.
                    <strong>Livraison de supports :</strong> réception au studio du lundi au vendredi
                    de 8 h à 17 h.</li>
              </ol>
            </div>

          </div>
        </div>
      </div>
    </section>
  </main>

  <a class="retour-haut" href="#haut" data-retour-haut>▲ Retour en haut</a>

  <footer class="pied">
    {bloc_pied()}
  </footer>

  {bloc_wa()}
  <script src="js/main.js"></script>
  <script src="js/formulaire.js"></script>
</body>
</html>
'''

# ------------------------------------------------------------------ ÉCRITURE
if __name__ == '__main__':
    os.makedirs(os.path.join(SITE, 'js'), exist_ok=True)
    for nom, contenu in (('index.html', page_accueil()),
                         ('catalogue.html', page_catalogue()),
                         ('contact.html', page_contact())):
        chemin = os.path.join(SITE, nom)
        with open(chemin, 'w', encoding='utf-8') as f:
            f.write(contenu)
        print(f'{nom:16s} {os.path.getsize(chemin)/1024:6.1f} Ko')
