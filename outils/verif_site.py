#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôle qualité du site ROOD-WOOKO DIGITAL : rendu aux 3 breakpoints,
absence d'erreur console, et tests fonctionnels (carrousel, filtres, menu mobile,
liens sociaux, téléphone, WhatsApp)."""
import os, sys, json
from playwright.sync_api import sync_playwright

SITE = '/workspace/rood-wooko-digital'
SHOTS = '/workspace/work/shots'
os.makedirs(SHOTS, exist_ok=True)

VUES = [('mobile', 390, 844), ('tablette', 820, 1100), ('desktop', 1440, 1000)]
PAGES = ['index.html', 'catalogue.html', 'contact.html']
resultats = {'erreurs_console': [], 'tests': []}

def test(nom, condition, detail=''):
    resultats['tests'].append({'nom': nom, 'ok': bool(condition), 'detail': detail})
    print(('  OK   ' if condition else '  ECHEC ') + nom + ((' — ' + detail) if detail else ''))

with sync_playwright() as p:
    nav = p.chromium.launch()
    for page in PAGES:
        for nom, w, h in VUES:
            ctx = nav.new_context(viewport={'width': w, 'height': h},
                                  device_scale_factor=1,
                                  reduced_motion='reduce')
            pg = ctx.new_page()
            erreurs = []
            pg.on('console', lambda m: erreurs.append(m.text) if m.type == 'error' else None)
            pg.on('pageerror', lambda e: erreurs.append(str(e)))
            pg.goto(f'file://{SITE}/{page}')
            pg.wait_for_timeout(900)
            pg.screenshot(path=f'{SHOTS}/{page[:-5]}-{nom}.png', full_page=True)
            if erreurs:
                resultats['erreurs_console'].append({'page': page, 'vue': nom, 'erreurs': erreurs})
            ctx.close()
    print('\n== captures terminées ==')

    # ------------------------------------------- tests fonctionnels (desktop)
    ctx = nav.new_context(viewport={'width': 1440, 'height': 1000})
    pg = ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    pg.goto(f'file://{SITE}/index.html')
    pg.wait_for_timeout(700)

    # carrousel
    avant = pg.eval_on_selector('.heros-piste', 'e => e.style.transform')
    pg.click('.heros-fleche.next')
    pg.wait_for_timeout(700)
    apres = pg.eval_on_selector('.heros-piste', 'e => e.style.transform')
    test('carrousel héros : la flèche suivante change de diapositive', avant != apres, f'{avant} -> {apres}')

    # logo animé en en-tête
    src = pg.get_attribute('.marque-logo', 'src')
    test('logo animé en en-tête', src.endswith('.gif'), src)

    # lien retour en haut
    pg.click('.retour-haut')
    pg.wait_for_timeout(2500)
    y = pg.evaluate('window.scrollY')
    test('lien « Retour en haut » ramène en haut', y < 10, f'scrollY={y}')

    # liens sociaux sur une fiche
    pg.goto(f'file://{SITE}/catalogue.html')
    pg.wait_for_timeout(700)
    n_cartes = pg.locator('.grille-produits .carte-produit').count()
    test('catalogue : 19 fiches présentes', n_cartes == 19, f'{n_cartes} fiches')

    n_socials = pg.locator('.grille-produits .carte-produit .social-bouton').count()
    test('5 liens sociaux sur chaque fiche (19 × 5)', n_socials == 19 * 5, f'{n_socials} liens')

    # chaque fiche a bien les 5 réseaux
    par_carte = pg.evaluate("""() => {
      const attendu = ['facebook','tiktok','galerie','whatsapp','instagram'];
      const cartes = [...document.querySelectorAll('.grille-produits .carte-produit')];
      return cartes.filter(c => {
        const r = [...c.querySelectorAll('.social-bouton')].map(b => b.dataset.reseau);
        return attendu.every(x => r.includes(x)) && r.length === 5;
      }).length;
    }""")
    test('chaque fiche porte bien les 5 réseaux (FB, TikTok, galerie, WA, Insta)', par_carte == 19, f'{par_carte}/19')

    # URL WhatsApp sans « + »
    wa = pg.get_attribute('.social-bouton[data-reseau="whatsapp"]', 'href')
    test('lien WhatsApp sans « + » dans l’URL', wa == 'https://wa.me/22656433122', wa)

    # cible et rel
    cibles = pg.evaluate("""() => [...document.querySelectorAll('.social-bouton')]
        .every(b => b.target === '_blank' && b.rel.includes('noopener'))""")
    test('tous les liens sociaux s’ouvrent en nouvel onglet (target + rel noopener)', cibles)

    # filtres
    pg.click('.puce-filtre[data-filtre="web"]')
    pg.wait_for_timeout(400)
    visibles = pg.evaluate("() => [...document.querySelectorAll('.grille-produits .carte-produit')].filter(c => !c.hidden).length")
    test('filtre catégorie « Web » : 4 fiches visibles', visibles == 4, f'{visibles} visibles')
    pg.click('.puce-filtre[data-filtre="toutes"]')
    pg.wait_for_timeout(300)
    total = pg.evaluate("() => [...document.querySelectorAll('.grille-produits .carte-produit')].filter(c => !c.hidden).length")
    test('filtre « Toutes » : 19 fiches visibles', total == 19, f'{total} visibles')

    # tri
    pg.select_option('#tri-catalogue', 'prix-asc')
    pg.wait_for_timeout(300)
    premier = pg.get_attribute('.grille-produits .carte-produit', 'data-prix')
    test('tri par prix croissant : le premier est le moins cher', premier == '15000', premier)

    # recherche depuis l'en-tête
    pg.goto(f'file://{SITE}/index.html')
    pg.wait_for_timeout(500)
    pg.fill('#recherche-champ', 'bannière')
    pg.click('.recherche-btn')
    pg.wait_for_timeout(900)
    test('la recherche de l’en-tête redirige vers le catalogue', 'catalogue.html' in pg.url, pg.url)

    # formulaire de contact
    pg.goto(f'file://{SITE}/contact.html')
    pg.wait_for_timeout(500)
    pg.click('#formulaire-contact button[type="submit"]')
    pg.wait_for_timeout(300)
    invalides = pg.locator('#formulaire-contact .champ.invalide').count()
    test('le formulaire bloque un envoi incomplet', invalides >= 5, f'{invalides} champs signalés')
    pg.fill('#nom', 'Aminata Ouédraogo')
    pg.fill('#email', 'aminata@example.bf')
    pg.fill('#telephone', '+226 70 12 34 56')
    pg.select_option('#sujet', index=4)
    pg.fill('#message', 'Nous souhaitons un shooting corporate de 20 personnes à Ouagadougou.')
    pg.wait_for_timeout(200)
    invalides2 = pg.locator('#formulaire-contact .champ.invalide').count()
    test('le formulaire valide une demande complète', invalides2 == 0, f'{invalides2} champs encore signalés')

    # coordonnées présentes sur les 3 pages
    for page in PAGES:
        pg.goto(f'file://{SITE}/{page}')
        pg.wait_for_timeout(400)
        html = pg.content()
        tel = html.count('tel:+22678450446')
        wa = html.count('https://wa.me/22656433122')
        aff_tel = html.count('+226 78 45 04 46')
        aff_wa = html.count('+226 56 43 31 22')
        test(f'{page} : téléphone cliquable et affiché', tel >= 1 and aff_tel >= 1, f'{tel} lien(s) / {aff_tel} affichage(s)')
        test(f'{page} : WhatsApp cliquable et affiché', wa >= 1 and aff_wa >= 1, f'{wa} lien(s) / {aff_wa} affichage(s)')

    # page contact : adresse et ville
    pg.goto(f'file://{SITE}/contact.html')
    html = pg.content()
    test('contact : adresse « Rue 9.19, Porte 180 » présente', 'Rue 9.19, Porte 180' in html)
    test('contact : « BURKINA FASO, OUAGADOUGOU » présente', 'BURKINA FASO, OUAGADOUGOU' in html)
    pg.goto(f'file://{SITE}/index.html')
    html = pg.content()
    test('pied de page : « BURKINA FASO, OUAGADOUGOU » présente', 'BURKINA FASO, OUAGADOUGOU' in html)
    test('pied de page : « Rue 9.19, Porte 180 » présente', 'Rue 9.19, Porte 180' in html)

    # absence de marque Amazon
    for page in PAGES:
        pg.goto(f'file://{SITE}/{page}')
        html = pg.content().lower()
        test(f'{page} : aucune trace de branding Amazon',
             'amazon' not in html and 'smile' not in html and 'aws' not in html)

    # menu mobile
    ctx2 = nav.new_context(viewport={'width': 390, 'height': 844})
    pg2 = ctx2.new_page()
    pg2.goto(f'file://{SITE}/index.html')
    pg2.wait_for_timeout(600)
    cache = pg2.is_visible('.ceinture')
    pg2.click('#bouton-menu')
    pg2.wait_for_timeout(500)
    ouvert = pg2.is_visible('.ceinture-inner .nav-lien')
    test('menu mobile : le burger ouvre la navigation', (not cache) and ouvert,
          f'ceinture visible avant={cache}, liens visibles après={ouvert}')
    pg2.click('[data-fermer-menu]')
    pg2.wait_for_timeout(400)
    test('menu mobile : le bouton « fermer » referme', not pg2.is_visible('.ceinture-inner .nav-lien'))
    ctx2.close()

    # accessibilité : alt sur toutes les images
    pg.goto(f'file://{SITE}/catalogue.html')
    sans_alt = pg.evaluate("() => [...document.images].filter(i => !i.getAttribute('alt')).length")
    test('toutes les images ont un attribut alt', sans_alt == 0, f'{sans_alt} sans alt')

    # balises sémantiques
    pg.goto(f'file://{SITE}/index.html')
    sem = pg.evaluate("""() => ({
      header: document.querySelectorAll('header').length,
      nav: document.querySelectorAll('nav').length,
      main: document.querySelectorAll('main').length,
      footer: document.querySelectorAll('footer').length,
      section: document.querySelectorAll('section').length
    })""")
    test('balises sémantiques présentes', sem['header'] >= 1 and sem['nav'] >= 1 and sem['main'] == 1 and sem['footer'] >= 1 and sem['section'] >= 3, json.dumps(sem))

    # aucune requête réseau externe
    requetes = []
    pg2 = ctx.new_page()
    pg2.on('request', lambda r: requetes.append(r.url))
    pg2.goto(f'file://{SITE}/index.html')
    pg2.wait_for_timeout(1200)
    externes = [u for u in requetes if not u.startswith('file://')]
    test('aucune ressource externe (site autonome hors-ligne)', not externes, ', '.join(externes[:3]))

    ctx.close()
    nav.close()

print('\n== erreurs console ==')
if resultats['erreurs_console']:
    for e in resultats['erreurs_console']:
        print(' ', e['page'], e['vue'], e['erreurs'])
else:
    print('  aucune')

echecs = [t for t in resultats['tests'] if not t['ok']]
print(f"\n== bilan : {len(resultats['tests'])-len(echecs)}/{len(resultats['tests'])} tests réussis ==")
for t in echecs:
    print('  ECHEC :', t['nom'], '—', t['detail'])
sys.exit(1 if echecs else 0)
