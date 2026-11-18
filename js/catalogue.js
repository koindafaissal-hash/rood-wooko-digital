/* =============================================================================
   ROOD-WOOKO DIGITAL — js/catalogue.js
   Filtrage par catégorie, recherche textuelle et tri du catalogue.
   JavaScript vanilla, sans aucune dépendance externe.
   -----------------------------------------------------------------------------
   ⚠️  URL SOCIALES À REMPLACER  ⚠️
   Les cinq liens sociaux placés sous chaque photo du catalogue ne sont
   PAS redéclarés ici : ils sont définis UNE SEULE FOIS dans js/main.js,
   dans la constante RWD_LINKS située tout en haut de ce fichier.
       REMPLACER CETTE URL PAR VOTRE VRAIE URL — Facebook
       REMPLACER CETTE URL PAR VOTRE VRAIE URL — TikTok
       REMPLACER CETTE URL PAR VOTRE VRAIE URL — Galerie de serveur
       REMPLACER CETTE URL PAR VOTRE VRAIE URL — Instagram
   (Le lien WhatsApp est une donnée réelle : https://wa.me/22656433122)
   Conséquence : modifier la valeur dans js/main.js met à jour
   instantanément les 16 fiches du catalogue. Ne pas dupliquer les URL.
   ========================================================================== */

const RWD_LINKS_CATALOGUE = window.RWD_LINKS || null;
if (!RWD_LINKS_CATALOGUE && window.console) {
  console.warn('ROOD-WOOKO : js/main.js doit être chargé avant js/catalogue.js ' +
               'pour que les liens sociaux soient corrects.');
}

const CATALOGUE = {
  grille:      '#grille-produits',
  puces:       '#filtres',
  compte:      '#compte-resultats',
  vide:        '#message-vide',
  aside:       '#aside-categories',
  tri:         '#tri-catalogue'
};

let categorieActive = 'toutes';
let rechercheActive = '';

/* ------------------------------------------------------------------ OUTILS */
function normaliser(texte) {
  return (texte || '').toString()
    .toLowerCase()
    .normalize ? (texte || '').toString().toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
               : (texte || '').toString().toLowerCase();
}

function prixNumerique(carte) {
  const brut = (carte.getAttribute('data-prix') || '0').replace(/[^0-9]/g, '');
  return parseInt(brut, 10) || 0;
}

/* ------------------------------------------------------- FILTRES PAR CATÉGORIE */
function appliquerFiltres() {
  const cartes = Array.prototype.slice.call(document.querySelectorAll('.grille-produits .carte-produit'));
  let visibles = 0;

  cartes.forEach(function (carte) {
    const cat = (carte.getAttribute('data-categorie') || '').toLowerCase();
    const nom = normaliser(carte.getAttribute('data-nom'));
    const mots = normaliser(carte.getAttribute('data-mots'));
    const description = normaliser(carte.getAttribute('data-description'));

    const okCat = (categorieActive === 'toutes') || (cat === categorieActive);
    const okRecherche = !rechercheActive ||
      nom.indexOf(rechercheActive) !== -1 ||
      mots.indexOf(rechercheActive) !== -1 ||
      description.indexOf(rechercheActive) !== -1;

    const visible = okCat && okRecherche;
    carte.hidden = !visible;
    carte.style.display = visible ? '' : 'none';
    if (visible) visibles++;
  });

  /* compteur */
  const compteur = document.querySelector(CATALOGUE.compte);
  if (compteur) {
    compteur.textContent = visibles + (visibles > 1 ? ' articles affichés' : ' article affiché');
  }

  /* état vide */
  const vide = document.querySelector(CATALOGUE.vide);
  if (vide) vide.setAttribute('data-visible', visibles === 0 ? 'true' : 'false');

  /* état actif des puces */
  document.querySelectorAll('.puce-filtre').forEach(function (puce) {
    const valeur = puce.getAttribute('data-filtre') || 'toutes';
    puce.setAttribute('aria-pressed', valeur === categorieActive ? 'true' : 'false');
  });

  /* état actif de la colonne latérale */
  document.querySelectorAll('#aside-categories a').forEach(function (lien) {
    const valeur = (lien.getAttribute('data-filtre') || 'toutes').toLowerCase();
    if (valeur === categorieActive) lien.setAttribute('aria-current', 'true');
    else lien.removeAttribute('aria-current');
  });
}

/* ------------------------------------------------------------------- TRI */
function trier(ordre) {
  const grille = document.querySelector(CATALOGUE.grille);
  if (!grille) return;
  const cartes = Array.prototype.slice.call(grille.querySelectorAll('.carte-produit'));
  cartes.sort(function (a, b) {
    if (ordre === 'prix-asc')  return prixNumerique(a) - prixNumerique(b);
    if (ordre === 'prix-desc') return prixNumerique(b) - prixNumerique(a);
    if (ordre === 'nom')       return normaliser(a.getAttribute('data-nom')).localeCompare(normaliser(b.getAttribute('data-nom')));
    return Number(b.getAttribute('data-populaire') || 0) - Number(a.getAttribute('data-populaire') || 0);
  });
  cartes.forEach(function (carte) { grille.appendChild(carte); });
}

/* ------------------------------------------------------------ INITIALISATION */
function initCatalogue() {
  const grille = document.querySelector(CATALOGUE.grille);
  if (!grille) return;

  /* puces de filtre */
  document.querySelectorAll('.puce-filtre').forEach(function (puce) {
    puce.addEventListener('click', function () {
      categorieActive = (puce.getAttribute('data-filtre') || 'toutes').toLowerCase();
      appliquerFiltres();
    });
  });

  /* liens de la colonne latérale */
  document.querySelectorAll('#aside-categories a').forEach(function (lien) {
    lien.addEventListener('click', function (e) {
      e.preventDefault();
      categorieActive = (lien.getAttribute('data-filtre') || 'toutes').toLowerCase();
      appliquerFiltres();
      window.scrollTo({ top: grille.offsetTop - 140, behavior: 'smooth' });
    });
  });

  /* tri */
  const selectTri = document.querySelector(CATALOGUE.tri);
  if (selectTri) {
    selectTri.addEventListener('change', function () { trier(selectTri.value); });
  }

  /* paramètres d'URL (?cat=...&q=...) : utilisés par la recherche de l'en-tête */
  const params = new URLSearchParams(window.location.search);
  const cat = (params.get('cat') || '').toLowerCase();
  const q = normaliser(params.get('q') || '').trim();
  if (cat && cat !== 'toutes') categorieActive = cat;
  if (q) {
    rechercheActive = q;
    const champ = document.querySelector('#recherche-champ');
    if (champ) champ.value = params.get('q');
    const select = document.querySelector('#recherche-categorie');
    if (select && cat) select.value = cat;
    /* information pour l'utilisateur */
    const info = document.querySelector('#recherche-info');
    if (info) {
      info.textContent = 'Recherche active : « ' + params.get('q') + ' »';
      info.setAttribute('data-visible', 'true');
    }
  }

  /* compteurs par catégorie dans la colonne latérale */
  const cartes = Array.prototype.slice.call(grille.querySelectorAll('.carte-produit'));
  document.querySelectorAll('#aside-categories a').forEach(function (lien) {
    const valeur = (lien.getAttribute('data-filtre') || 'toutes').toLowerCase();
    const cible = lien.querySelector('.nombre');
    if (!cible) return;
    if (valeur === 'toutes') cible.textContent = String(cartes.length);
    else cible.textContent = String(cartes.filter(function (c) {
      return (c.getAttribute('data-categorie') || '').toLowerCase() === valeur;
    }).length);
  });

  appliquerFiltres();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initCatalogue);
} else {
  initCatalogue();
}
