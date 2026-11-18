#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérification finale : les 12 points d'auto-contrôle du cahier des charges."""
import os, re, sys, glob
from playwright.sync_api import sync_playwright

SITE = '/workspace/rood-wooko-digital'
PAGES = ['index.html', 'catalogue.html', 'contact.html']
ok_all = True

def check(n, cond, detail=''):
    global ok_all
    if not cond: ok_all = False
    print(('  [OK]   ' if cond else '  [ÉCHEC] ') + n + ((' — ' + detail) if detail else ''))

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 1000})
    pg = ctx.new_page()
    pages = {}
    for f in PAGES:
        pg.goto(f'file://{SITE}/{f}')
        pg.wait_for_timeout(700)
        pages[f] = pg.content()

    print('\n■ POINT 1 — « ROOD-WOOKO DIGITAL » dans l’en-tête, le pied de page et les <title>')
    for f in PAGES:
        title = re.search(r'<title>(.*?)</title>', pages[f], re.S).group(1)
        check(f'{f} : nom dans le <title>', 'ROOD-WOOKO DIGITAL' in title, title.strip()[:70])
    check('index : nom dans l’en-tête', 'marque-logo' in pages['index.html'])
    for f in PAGES:
        check(f'{f} : nom dans le pied de page', pages[f].count('ROOD-WOOKO DIGITAL') >= 2)

    print('\n■ POINT 2 — ville et adresse dans le pied de page et sur la page Contact')
    check('pied de page : « BURKINA FASO, OUAGADOUGOU »', 'BURKINA FASO, OUAGADOUGOU' in pages['index.html'])
    check('pied de page : « Rue 9.19, Porte 180 »', 'Rue 9.19, Porte 180' in pages['index.html'])
    check('contact : « BURKINA FASO, OUAGADOUGOU »', 'BURKINA FASO, OUAGADOUGOU' in pages['contact.html'])
    check('contact : « Rue 9.19, Porte 180 »', 'Rue 9.19, Porte 180' in pages['contact.html'])

    print('\n■ POINT 3 — téléphone cliquable tel:+22678450446')
    for f in PAGES:
        check(f'{f} : lien tel: présent', 'tel:+22678450446' in pages[f])

    print('\n■ POINT 4 — WhatsApp https://wa.me/22656433122 (sans « + »)')
    for f in PAGES:
        n_wa = pages[f].count('https://wa.me/22656433122')
        n_plus = len(re.findall(r'wa\.me/\+', pages[f]))
        check(f'{f} : lien WhatsApp sans « + » dans l’URL', n_wa > 0 and n_plus == 0,
              f'{n_wa} lien(s), {n_plus} avec « + »')
    check('index : WhatsApp dans l’en-tête', 'wa.me/22656433122' in pages['index.html'].split('</header>')[0])
    check('index : WhatsApp dans le pied de page', 'wa.me/22656433122' in pages['index.html'].split('</main>')[1])
    check('contact : WhatsApp sur la page', 'wa.me/22656433122' in pages['contact.html'])
    check('bouton WhatsApp flottant sur les 3 pages',
          all('wa-flottant' in pages[f] for f in PAGES))

    print('\n■ POINT 5 — les 3 pages existent et sont reliées par la navigation')
    for f in PAGES:
        check(f'{f} existe', os.path.exists(os.path.join(SITE, f)))
    for f in PAGES:
        nav = pages[f].split('</nav>')[0]
        check(f'{f} : liens vers les 3 pages', all(x in nav for x in ['index.html', 'catalogue.html', 'contact.html']))

    print('\n■ POINT 6 — 100 % des images du catalogue portent les 5 liens')
    pg.goto(f'file://{SITE}/catalogue.html')
    pg.wait_for_timeout(600)
    n_cartes = pg.locator('.grille-produits .carte-produit').count()
    n_socials = pg.locator('.grille-produits .carte-produit .social-bouton').count()
    check('chaque fiche porte exactement 5 liens', n_cartes > 0 and n_socials == n_cartes * 5,
          f'{n_cartes} fiches, {n_socials} liens')
    attendu = ['facebook', 'tiktok', 'galerie', 'whatsapp', 'instagram']
    conformes = pg.evaluate("""(attendu) => {
      return [...document.querySelectorAll('.grille-produits .carte-produit')].filter(c => {
        const r = [...c.querySelectorAll('.social-bouton')].map(b => b.dataset.reseau).sort();
        return JSON.stringify(r) === JSON.stringify([...attendu].sort());
      }).length;
    }""", attendu)
    check('les 5 réseaux sont bien présents sur chaque fiche', conformes == n_cartes, f'{conformes}/{n_cartes}')

    print('\n■ POINT 7 — aucune trace de branding Amazon')
    for f in PAGES:
        bas = pages[f].lower()
        check(f'{f} : aucun mot « amazon », « smile », « aws », « prime »',
              not any(k in bas for k in ['amazon', 'smile', 'aws prime', 'prime video']))

    print('\n■ POINT 8 — aucune dépendance externe')
    reqs = []
    pg2 = ctx.new_page()
    pg2.on('request', lambda r: reqs.append(r.url))
    pg2.goto(f'file://{SITE}/index.html')
    pg2.wait_for_timeout(1500)
    externes = [u for u in reqs if not u.startswith('file://')]
    check('aucune requête réseau externe', not externes, ', '.join(externes[:3]))
    liens_ext = re.findall(r'<link[^>]+href="(https?://[^"]+)"', pages['index.html'])
    scripts_ext = re.findall(r'<script[^>]+src="(https?://[^"]+)"', pages['index.html'])
    check('aucune ressource externe déclarée en dur',
          not liens_ext and not scripts_ext,
          ', '.join(liens_ext + scripts_ext))

    print('\n■ POINT 9 — carrousel héros, filtres et menu mobile fonctionnent')
    pg.goto(f'file://{SITE}/index.html')
    pg.wait_for_timeout(600)
    t0 = pg.eval_on_selector('.heros-piste', 'e => e.style.transform')
    pg.click('.heros-fleche.next')
    pg.wait_for_timeout(700)
    t1 = pg.eval_on_selector('.heros-piste', 'e => e.style.transform')
    check('carrousel héros pilotable', t0 != t1)
    check('carrousel : 4 diapositives', pg.locator('.heros-slide').count() == 4)
    check('carrousel : 4 indicateurs', pg.locator('.heros-point').count() == 4)
    auto = pg.evaluate("""() => new Promise(res => {
      const t0 = document.querySelector('.heros-piste').style.transform;
      setTimeout(() => res(document.querySelector('.heros-piste').style.transform !== t0), 6200);
    })""")
    check('carrousel : défilement automatique toutes les 5 s', auto)
    pg.goto(f'file://{SITE}/catalogue.html')
    pg.wait_for_timeout(600)
    pg.click('.puce-filtre[data-filtre="impression"]')
    pg.wait_for_timeout(400)
    v = pg.evaluate("() => [...document.querySelectorAll('.grille-produits .carte-produit')].filter(c=>!c.hidden).length")
    check('filtres du catalogue opérationnels', v == 5, f'{v} fiches « Impression »')
    ctx2 = b.new_context(viewport={'width': 390, 'height': 844})
    pg3 = ctx2.new_page()
    pg3.goto(f'file://{SITE}/index.html')
    pg3.wait_for_timeout(600)
    pg3.click('#bouton-menu')
    pg3.wait_for_timeout(400)
    check('menu mobile hamburger fonctionnel', pg3.is_visible('.ceinture-inner .nav-lien'))
    ctx2.close()

    print('\n■ POINT 10 — URLs sociales regroupées dans des constantes commentées en tête de fichier')
    js = open(os.path.join(SITE, 'js', 'main.js'), encoding='utf-8').read()
    check('js/main.js : bloc de commentaires « REMPLACER CETTE URL »',
          js.count('REMPLACER CETTE URL PAR VOTRE VRAIE URL') >= 4)
    check('js/main.js : constantes en tête de fichier',
          js.index('RWD_URL_FACEBOOK') < js.index('function init()'))
    for u in ['RWD_URL_FACEBOOK', 'RWD_URL_TIKTOK', 'RWD_URL_GALERIE', 'RWD_URL_INSTAGRAM', 'RWD_URL_WHATSAPP']:
        check(f'js/main.js : constante {u} définie', f'const {u}' in js)
    js2 = open(os.path.join(SITE, 'js', 'catalogue.js'), encoding='utf-8').read()
    check('js/catalogue.js : rappel du point de modification', 'js/main.js' in js2 and 'REMPLACER CETTE URL' in js2)

    print('\n■ POINT 11 — tout le texte visible est en français, sans « Lorem ipsum »')
    for f in PAGES:
        txt = re.sub(r'<[^>]+>', ' ', pages[f])
        check(f'{f} : pas de « Lorem ipsum » ni de texte générique',
              'lorem' not in txt.lower() and 'votre texte ici' not in txt.lower() and 'image.jpg' not in txt.lower())
        check(f'{f} : aucun placeholder anglais « Click here » / « Read more »',
              'click here' not in txt.lower() and 'read more' not in txt.lower() and 'learn more' not in txt.lower())

    print('\n■ POINT 12 — responsive sur les 3 points de rupture')
    css = open(os.path.join(SITE, 'css', 'style.css'), encoding='utf-8').read()
    check('CSS : point de rupture ≤ 600 px', '@media (max-width: 600px)' in css)
    check('CSS : point de rupture 601–1024 px', '@media (max-width: 1024px)' in css)
    check('CSS : grille desktop (> 1024 px)', 'repeat(4, 1fr)' in css)
    for f in PAGES:
        for nom, w in (('mobile', 390), ('tablette', 820), ('desktop', 1440)):
            ctx3 = b.new_context(viewport={'width': w, 'height': 900})
            pgx = ctx3.new_page()
            pgx.goto(f'file://{SITE}/{f}')
            pgx.wait_for_timeout(500)
            deb = pgx.evaluate('document.documentElement.scrollWidth')
            check(f'{f} ({nom}) : pas de débordement horizontal', deb <= w + 1, f'scrollWidth={deb} / {w}')
            ctx3.close()

    b.close()

print('\n' + ('=' * 70))
print('RÉSULTAT : ' + ('LES 12 POINTS DU CAHIER DES CHARGES SONT VALIDÉS' if ok_all else 'DES POINTS RESTENT À CORRIGER'))
print('=' * 70)
sys.exit(0 if ok_all else 1)
