# ROOD-WOOKO DIGITAL — site vitrine statique

Site vitrine **HTML5 + CSS3 + JavaScript vanilla**, sans aucune dépendance externe
(aucun CDN, aucun framework, aucune police distante). Le dossier fonctionne **hors ligne**,
une fois les fichiers ouverts : il suffit de double-cliquer sur `index.html`.

- Client : **ROOD-WOOKO DIGITAL** — studio photo, design et web à Ouagadougou
- Pages : `index.html` (accueil), `catalogue.html` (catalogue filtrable), `contact.html` (contact et accès)
- Charte : rouge profond `#C0392B`, noir charbon `#1A1A1A`, jaune doré `#F1C40F`, fond `#F5F5F3`
- Animations : les **cinq propositions de logo animé** du client, en `.gif` local (≤ 250 Ko pièce)

---

## 1. Contenu du dossier

```
rood-wooko-digital/
├── index.html              Accueil : carrousel héros, catégories, 3 carrousels de catalogue, marque, contact rapide
├── catalogue.html          Catalogue : 19 fiches, filtres par catégorie, tri, recherche
├── contact.html            Contact : formulaire validé, coordonnées, horaires, plan d'accès textuel
├── README.md               Ce document
├── css/
│   └── style.css           Feuille de style unique (charte, composants, 3 points de rupture)
├── js/
│   ├── main.js             Constantes sociales, carrousel, rails, menu mobile, recherche, liens sociaux
│   ├── catalogue.js        Filtres par catégorie, tri, lecture des paramètres d'URL
│   └── formulaire.js       Validation du formulaire de contact (envoi WhatsApp / e-mail)
├── assets/
│   ├── favicon.svg         Favicon (masque de la marque)
│   ├── img/                32 visuels SVG générés localement (fiches, catégories, bannières)
│   └── logo/               Les 5 logotypes animés + leur version PNG statique
└── outils/                 Scripts de génération (optionnels, voir § 6)
```

## 2. Où remplacer les URL sociales — **un seul endroit**

Ouvrez **`js/main.js`** et modifiez les cinq lignes du bloc en haut de fichier :

```js
/* REMPLACER CETTE URL PAR VOTRE VRAIE URL — page Facebook officielle */
const RWD_URL_FACEBOOK = 'https://www.facebook.com/VOTRE-PAGE-FACEBOOK';
/* REMPLACER CETTE URL PAR VOTRE VRAIE URL — compte TikTok officiel */
const RWD_URL_TIKTOK   = 'https://www.tiktok.com/@VOTRE-COMPTE-TIKTOK';
/* REMPLACER CETTE URL PAR VOTRE VRAIE URL — galerie de serveur */
const RWD_URL_GALERIE  = 'GALERIE_SERVEUR_URL';
/* REMPLACER CETTE URL PAR VOTRE VRAIE URL — compte Instagram officiel */
const RWD_URL_INSTAGRAM= 'https://www.instagram.com/VOTRE-COMPTE-INSTAGRAM';
```

C'est **la seule modification à faire** : `js/main.js` réécrit au chargement les cinq liens
de chaque fiche du catalogue, des carrousels de l'accueil et du pied de page.
Le HTML contient déjà les mêmes adresses, afin que les liens fonctionnent même si JavaScript
est désactivé.

Le lien WhatsApp (`https://wa.me/22656433122`) et le téléphone (`tel:+22678450446`) sont des
données réelles : ne les modifiez pas.

> `js/catalogue.js` ne redéclare pas ces URL : il lit `window.RWD_LINKS`. C'est volontaire —
> il n'y a donc bien qu'un seul endroit à modifier.

## 3. Les cinq liens sous chaque photo

Chaque fiche du catalogue porte les cinq liens suivants, en SVG inline (aucune police
d'icônes) :

| # | Réseau | Destination |
|---|---|---|
| 1 | Facebook | `RWD_URL_FACEBOOK` |
| 2 | TikTok | `RWD_URL_TIKTOK` |
| 3 | Galerie de serveur | `RWD_URL_GALERIE` |
| 4 | WhatsApp | `https://wa.me/22656433122` |
| 5 | Instagram | `RWD_URL_INSTAGRAM` |

- **Bureau** : la rangée apparaît au survol de la photo.
- **Mobile / tactile** : la rangée reste visible en permanence, sous l'image.
- Chaque lien s'ouvre dans un nouvel onglet (`target="_blank" rel="noopener"`) et porte un
  `aria-label` explicite.

## 4. Le formulaire de contact

Le formulaire ne dépend d'aucun service tiers : la validation est faite en JavaScript, puis
le message est transmis soit par **WhatsApp** (`https://wa.me/22656433122?text=…`), soit par
la messagerie du poste de travail (`mailto:contact@rood-wooko.bf`).
Pour changer l'adresse de réception, modifiez `RWD_EMAIL_CONTACT` dans `js/formulaire.js`.

## 5. Instructions de déploiement

1. **Transférez le dossier complet** (`rood-wooko-digital/`) chez votre hébergeur par FTP,
   SFTP ou l'explorateur de fichiers (tous les dossiers, y compris `css`, `js`, `assets`).
2. **Remplacez les URL sociales** dans `js/main.js` (voir § 2) et, si nécessaire,
   l'adresse de réception dans `js/formulaire.js`.
3. **Déployez à la racine du domaine** (par exemple `public_html/`) : `index.html` sera alors
   la page d'accueil. Aucune configuration de build ni de base de données n'est nécessaire.
4. **Activez le HTTPS** dans le panneau de votre hébergeur (certificat gratuit inclus chez la
   plupart des hébergeurs) — indispensable pour que `tel:` et WhatsApp se comportent bien
   sur mobile.
5. **Testez** : ouvrez `https://votre-domaine/` puis `.../catalogue.html` et `.../contact.html`,
   et vérifiez que les cinq liens sous une photo du catalogue mènent aux bonnes pages.

> Le site est entièrement statique : un simple dossier de fichiers sur n'importe quel
> hébergement (mutualisé, CDN, GitHub Pages, Netlify) suffit. Aucun Node, aucun bundler.

## 6. Outils de génération (optionnels)

Le dossier `outils/` contient les scripts qui ont produit les pages et les visuels :

| Script | Rôle |
|---|---|
| `generateur_site.py` | Génère les 3 pages HTML à partir des données du catalogue (source unique : l'en-tête et le pied de page sont identiques sur les 3 pages) |
| `generateur_visuels.py` | Génère les 32 visuels SVG de `assets/img/` |
| `build_assets.py` | Recadre et optimise les 5 GIF de logo fournis par le client |

Ils nécessitent Python 3 et la bibliothèque Pillow. Ils ne sont pas nécessaires pour faire
tourner le site : supprimez le dossier `outils/` avant la mise en ligne si vous le souhaitez.

## 7. Ajouter une fiche au catalogue

Le catalogue vit dans `outils/generateur_site.py` (liste `CATALOGUE`). Une fiche tient sur une
ligne :

```python
('mon-slug', 'Mon titre — sous-titre', 'photo', 120000,
 'Description courte affichée sur la fiche.', 14, 70, 'mots-clés', 'cat-mon-slug.svg'),
```

Puis relancez `python3 outils/generateur_site.py`. Sans les outils, dupliquez simplement un
bloc `<article class="carte-produit">` dans `catalogue.html` et `index.html`, enCopiant les
attributs `data-*` (`data-categorie`, `data-prix`, `data-nom`, `data-mots`) : ce sont eux qui
pilotent le filtrage, la recherche et le tri.

## 8. Accessibilité, performance et référencement

- **Accessibilité** : balises sémantiques (`header`, `nav`, `main`, `section`, `footer`),
  lien d'évitement, `alt` sur toutes les images, `aria-label` sur tous les boutons icônes,
  navigation clavier complète (le carrousel répond aux flèches gauche/droite), contrastes
  conformes WCAG AA sur les textes.
- **Performance** : aucune requête réseau externe ; le poids total du dossier est d'environ
  **1,4 Mo**, dont 950 Ko pour les cinq logos animés. Les GIF sont limités à 12 images et
  64 couleurs. Un repli **PNG statique** est servi automatiquement aux navigateurs qui
  respectent `prefers-reduced-motion`.
- **Référencement** : `title` et `meta description` uniques et en français sur chaque page,
  hierarchy de titres continue, textes de lien explicites.

## 9. Notes de conception

- La structure reprend l'anatomie d'un grand site de e-commerce (barre supérieure, en-tête
  à trois zones avec recherche centrale, ceinture de navigation, carrousel héros, grilles de
  catégories, rails de catalogue, lien « Retour en haut », pied de page multi-colonnes,
  bouton WhatsApp flottant) **sans aucun élément de marque tiers** : ni logo, ni nom, ni
  couleur, ni illustration d'une marque existante.
- Le **cuivre `#B87333`** complète la charte imposée : c'est la couleur du logotype client,
  elle est utilisée pour l'emblème, les liens de pied de page et les libellés de catégorie.
  Les quatre couleurs imposées restent inchangées.
- Le motif **« masque de bronze »** (crête, visage, oreilles) est le fil graphique des
  bannières, des visuels de catalogue et du favicon : il donne une signature cohérente à
  l'ensemble du site.
- Les tarifs indiqués sont des **prix de départ** plausibles pour le marché burkinabè ; le
  pied de page du catalogue renvoie vers la demande de devis sur WhatsApp.
