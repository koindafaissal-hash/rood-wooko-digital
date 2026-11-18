/* =============================================================================
   ROOD-WOOKO DIGITAL — js/main.js
   JavaScript vanilla, sans aucune dépendance externe.
   -----------------------------------------------------------------------------
   ⚠️  URL SOCIALES À REMPLACER  ⚠️
   Les cinq liens sociaux demandés sous chaque photo du catalogue sont
   regroupés ICI, dans cette seule constante. Modifiez les cinq valeurs
   ci-dessous : le changement se répercute automatiquement sur les 16 fiches
   du catalogue, sur les carrousels de l'accueil et sur le pied de page.
   Aucune modification du HTML n'est nécessaire.
   ========================================================================== */

/* REMPLACER CETTE URL PAR VOTRE VRAIE URL — page Facebook officielle */
const RWD_URL_FACEBOOK = 'https://www.facebook.com/VOTRE-PAGE-FACEBOOK';
/* REMPLACER CETTE URL PAR VOTRE VRAIE URL — compte TikTok officiel */
const RWD_URL_TIKTOK = 'https://www.tiktok.com/@VOTRE-COMPTE-TIKTOK';
/* REMPLACER CETTE URL PAR VOTRE VRAIE URL — galerie de serveur (portefeuille) */
const RWD_URL_GALERIE = 'GALERIE_SERVEUR_URL';
/* REMPLACER CETTE URL PAR VOTRE VRAIE URL — compte Instagram officiel */
const RWD_URL_INSTAGRAM = 'https://www.instagram.com/VOTRE-COMPTE-INSTAGRAM';

/* Lien WhatsApp : donnée réelle, à ne pas modifier.
   L'URL ne contient PAS le « + » (format wa.me/226...), l'affichage si. */
const RWD_URL_WHATSAPP = 'https://wa.me/22656433122';
/* Téléphone cliquable : donnée réelle, à ne pas modifier. */
const RWD_URL_TELEPHONE = 'tel:+22678450446';

/* Regroupement unique des cinq liens — source de vérité du site. */
const RWD_LINKS = {
  facebook:  RWD_URL_FACEBOOK,
  tiktok:    RWD_URL_TIKTOK,
  galerie:   RWD_URL_GALERIE,
  whatsapp:  RWD_URL_WHATSAPP,
  instagram: RWD_URL_INSTAGRAM
};

/* Coordonnées affichées (données réelles du client — ne pas modifier). */
const RWD_CONTACT = {
  ville:      'BURKINA FASO, OUAGADOUGOU',
  telephone:  '+226 78 45 04 46',
  whatsapp:   '+226 56 43 31 22',
  adresse:    'Rue 9.19, Porte 180'
};

/* ------------------------------------------------------------------ ICONES */
const ICONES = {
  facebook: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M22 12.06C22 6.5 17.52 2 12 2S2 6.5 2 12.06c0 5 3.66 9.15 8.44 9.94v-7.03H7.9v-2.91h2.54V9.85c0-2.52 1.49-3.91 3.77-3.91 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.78-1.63 1.57v1.89h2.78l-.44 2.91h-2.34V22c4.78-.79 8.44-4.94 8.44-9.94z"/></svg>',
  tiktok:   '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M16.6 5.82A4.28 4.28 0 0 1 15.54 3h-3.09v12.4a2.59 2.59 0 0 1-2.59 2.5 2.59 2.59 0 0 1 0-5.18c.27 0 .52.04.76.12v-3.2a5.87 5.87 0 0 0-.76-.05A5.72 5.72 0 0 0 4.14 15.3 5.72 5.72 0 0 0 9.86 21a5.72 5.72 0 0 0 5.72-5.72V9.01a7.35 7.35 0 0 0 4.28 1.38V7.3a4.29 4.29 0 0 1-3.26-1.48z"/></svg>',
  galerie:  '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M21 19V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2zM8.5 13.5l2.5 3 3.5-4.5 4.5 6H5l3.5-4.5z"/></svg>',
  whatsapp: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M17.47 14.38c-.3-.15-1.75-.86-2.02-.96-.27-.1-.47-.15-.67.15-.2.3-.77.96-.94 1.16-.17.2-.35.22-.64.08-.3-.15-1.25-.46-2.38-1.47-.88-.78-1.47-1.75-1.65-2.05-.17-.3-.02-.46.13-.6.13-.13.3-.35.44-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.6-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.22 3.08c.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.69.63.71.22 1.36.19 1.87.12.57-.09 1.75-.72 2-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35zM12.04 21.5h-.01c-1.75 0-3.47-.47-4.98-1.36l-.36-.21-3.7.97.99-3.61-.23-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.89 9.9-9.89 2.64 0 5.13 1.03 7 2.9a9.83 9.83 0 0 1 2.89 7c0 5.45-4.44 9.89-9.9 9.89zM20.52 3.45A11.8 11.8 0 0 0 12.04 0C5.46 0 .08 5.38.08 11.96c0 2.1.55 4.16 1.6 5.97L0 24l6.2-1.63a11.9 11.9 0 0 0 5.84 1.48h.01c6.58 0 11.94-5.38 11.94-11.96 0-3.2-1.25-6.2-3.47-8.45z"/></svg>',
  instagram:'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41-.56-.22-.96-.48-1.38-.9-.42-.42-.68-.82-.9-1.38-.16-.42-.36-1.06-.41-2.23-.06-1.27-.07-1.65-.07-4.85s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41 1.27-.06 1.65-.07 4.85-.07m0 2.12c-3.15 0-3.5.01-4.74.07-1.14.05-1.76.24-2.17.4-.55.21-.94.47-1.35.88-.41.41-.67.8-.88 1.35-.16.41-.35 1.03-.4 2.17-.06 1.24-.07 1.59-.07 4.74s.01 3.5.07 4.74c.05 1.14.24 1.76.4 2.17.21.55.47.94.88 1.35.41.41.8.67 1.35.88.41.16 1.03.35 2.17.4 1.24.06 1.59.07 4.74.07s3.5-.01 4.74-.07c1.14-.05 1.76-.24 2.17-.4.55-.21.94-.47 1.35-.88.41-.41.67-.8.88-1.35.16-.41.35-1.03.4-2.17.06-1.24.07-1.59.07-4.74s-.01-3.5-.07-4.74c-.05-1.14-.24-1.76-.4-2.17a3.6 3.6 0 0 0-.88-1.35 3.6 3.6 0 0 0-1.35-.88c-.41-.16-1.03-.35-2.17-.4-1.24-.06-1.59-.07-4.74-.07zM12 7.38a4.62 4.62 0 1 1 0 9.24 4.62 4.62 0 0 1 0-9.24zm0 7.62a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM18.54 6.78a1.08 1.08 0 1 1-2.15 0 1.08 1.08 0 0 1 2.15 0z"/></svg>'
};

const LIBELLES = {
  facebook:  'Facebook',
  tiktok:    'TikTok',
  galerie:   'Galerie de serveur',
  whatsapp:  'WhatsApp',
  instagram: 'Instagram'
};

/* Expose les données pour les autres scripts (aucune dépendance externe). */
window.RWD_LINKS = RWD_LINKS;
window.RWD_CONTACT = RWD_CONTACT;
window.RWD_ICONES = ICONES;
window.RWD_LIBELLES = LIBELLES;

/* ------------------------------------------------------------------ OUTILS */
function $(sel, racine) { return (racine || document).querySelector(sel); }
function $$(sel, racine) { return Array.prototype.slice.call((racine || document).querySelectorAll(sel)); }

function prefersReducedMotion() {
  return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/* --------------------------------------------- LIENS SOCIAUX SOUS CHAQUE PHOTO
   Le HTML contient déjà les cinq liens (pour fonctionner sans JavaScript) ;
   cette fonction réécrit leurs URL à partir des constantes RWD_LINKS :
   une seule modification à faire, dans ce fichier.                        */
function appliquerLiensSociaux(racine) {
  $$('[data-reseau]', racine || document).forEach(function (lien) {
    const reseau = lien.getAttribute('data-reseau');
    if (RWD_LINKS[reseau]) {
      lien.setAttribute('href', RWD_LINKS[reseau]);
      lien.setAttribute('target', '_blank');
      lien.setAttribute('rel', 'noopener');
    }
    lien.setAttribute('aria-label', LIBELLES[reseau] + ' — ROOD-WOOKO DIGITAL (nouvel onglet)');
  });
}

/* Construit la rangée complète des cinq liens dans un conteneur vide. */
function construireLiensSociaux(conteneur) {
  if (!conteneur) return;
  /* si les liens sont déjà présents dans le HTML (mode sans JavaScript),
     on ne les duplique pas */
  if (conteneur.children.length > 0) { appliquerLiensSociaux(conteneur); return; }
  ['facebook', 'tiktok', 'galerie', 'whatsapp', 'instagram'].forEach(function (reseau) {
    const a = document.createElement('a');
    a.className = 'social-bouton';
    a.setAttribute('data-reseau', reseau);
    a.href = RWD_LINKS[reseau];
    a.target = '_blank';
    a.rel = 'noopener';
    a.title = LIBELLES[reseau];
    a.innerHTML = ICONES[reseau];
    conteneur.appendChild(a);
  });
  appliquerLiensSociaux(conteneur);
}

/* ------------------------------------------------- MENU MOBILE (HAMBURGER) */
function initMenuMobile() {
  const bouton = $('#bouton-menu');
  const ceinture = $('#ceinture-nav');
  if (!bouton || !ceinture) return;

  function basculer(ouvrir) {
    const etat = typeof ouvrir === 'boolean' ? ouvrir : !ceinture.classList.contains('mobile-ouvert');
    ceinture.classList.toggle('mobile-ouvert', etat);
    bouton.setAttribute('aria-expanded', etat ? 'true' : 'false');
    document.body.style.overflow = etat ? 'hidden' : '';
    if (etat) {
      const premier = ceinture.querySelector('a, button');
      if (premier) premier.focus();
    }
  }

  bouton.addEventListener('click', function () { basculer(); });
  $$('[data-fermer-menu]', ceinture).forEach(function (fermer) {
    fermer.addEventListener('click', function () { basculer(false); bouton.focus(); });
  });
  window.addEventListener('resize', function () {
    if (window.innerWidth > 600) basculer(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && ceinture.classList.contains('mobile-ouvert')) {
      basculer(false);
      bouton.focus();
    }
  });
}

/* ------------------------------------------------ MENU « TOUTES CATÉGORIES » */
function initMenuCategories() {
  const bloc = $('.nav-categories');
  if (!bloc) return;
  const bouton = bloc.querySelector('button');
  const menu = bloc.querySelector('.menu-categories');
  if (!bouton || !menu) return;

  function basculer(ouvrir) {
    const etat = typeof ouvrir === 'boolean' ? ouvrir : bloc.getAttribute('data-ouvert') !== 'true';
    bloc.setAttribute('data-ouvert', etat ? 'true' : 'false');
    bouton.setAttribute('aria-expanded', etat ? 'true' : 'false');
  }
  bouton.addEventListener('click', function (e) {
    e.stopPropagation();
    basculer();
  });
  document.addEventListener('click', function (e) {
    if (!bloc.contains(e.target)) basculer(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { basculer(false); bouton.focus(); }
  });
  $$('.menu-categories a', bloc).forEach(function (lien) {
    lien.addEventListener('click', function () { basculer(false); });
  });
}

/* ------------------------------------------------------- RECHERCHE (entête) */
function initRecherche() {
  const formulaire = $('#form-recherche');
  if (!formulaire) return;
  formulaire.addEventListener('submit', function (e) {
    e.preventDefault();
    const champ = $('#recherche-champ');
    const categorie = $('#recherche-categorie');
    const q = champ && champ.value.trim();
    const cat = categorie && categorie.value;
    const cible = 'catalogue.html';
    const params = [];
    if (q) params.push('q=' + encodeURIComponent(q));
    if (cat && cat !== 'toutes') params.push('cat=' + encodeURIComponent(cat));
    window.location.href = params.length ? cible + '?' + params.join('&') : cible;
  });
}

/* ------------------------------------------------------ CARROUSEL HÉROS */
function initHeros() {
  const heros = $('#heros');
  if (!heros) return;
  const piste = $('.heros-piste', heros);
  const slides = $$('.heros-slide', heros);
  const points = $$('.heros-point', heros);
  const prec = $('.heros-fleche.prev', heros);
  const suiv = $('.heros-fleche.next', heros);
  if (!piste || slides.length === 0) return;

  let index = 0;
  let minuterie = null;
  const DELAI = 5000;

  function afficher(i) {
    index = (i + slides.length) % slides.length;
    piste.style.transform = 'translateX(' + (-index * 100) + '%)';
    points.forEach(function (p, n) {
      p.setAttribute('aria-selected', n === index ? 'true' : 'false');
      p.setAttribute('tabindex', n === index ? '0' : '-1');
    });
    slides.forEach(function (s, n) {
      s.setAttribute('aria-hidden', n === index ? 'false' : 'true');
    });
  }
  function demarrer() {
    if (prefersReducedMotion()) return;
    arreter();
    minuterie = window.setInterval(function () { afficher(index + 1); }, DELAI);
  }
  function arreter() {
    if (minuterie) { window.clearInterval(minuterie); minuterie = null; }
  }

  if (prec) prec.addEventListener('click', function () { afficher(index - 1); demarrer(); });
  if (suiv) suiv.addEventListener('click', function () { afficher(index + 1); demarrer(); });
  points.forEach(function (p, n) {
    p.addEventListener('click', function () { afficher(n); demarrer(); });
    p.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); afficher(n); demarrer(); }
    });
  });

  heros.addEventListener('mouseenter', arreter);
  heros.addEventListener('mouseleave', demarrer);
  heros.addEventListener('focusin', arreter);
  heros.addEventListener('focusout', demarrer);

  /* navigation clavier */
  heros.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') { afficher(index - 1); demarrer(); }
    if (e.key === 'ArrowRight') { afficher(index + 1); demarrer(); }
  });

  /* balayage tactile */
  let debutX = null;
  heros.addEventListener('touchstart', function (e) { debutX = e.touches[0].clientX; }, { passive: true });
  heros.addEventListener('touchend', function (e) {
    if (debutX === null) return;
    const dx = e.changedTouches[0].clientX - debutX;
    if (Math.abs(dx) > 45) { afficher(index + (dx < 0 ? 1 : -1)); demarrer(); }
    debutX = null;
  }, { passive: true });

  afficher(0);
  demarrer();
}

/* -------------------------------------------- RAILS DE CATALOGUE DÉFILANTS */
function initRails() {
  $$('[data-rail]').forEach(function (rail) {
    const piste = $('.rail-piste', rail);
    const prec = $('.rail-btn.prev', rail);
    const suiv = $('.rail-btn.next', rail);
    if (!piste) return;

    function pas() {
      const item = piste.firstElementChild;
      if (!item) return 300;
      const style = window.getComputedStyle(piste);
      const gap = parseFloat(style.columnGap || style.gap || '0') || 18;
      return item.getBoundingClientRect().width + gap;
    }
    function majBoutons() {
      if (prec) prec.disabled = piste.scrollLeft <= 4;
      if (suiv) suiv.disabled = piste.scrollLeft + piste.clientWidth >= piste.scrollWidth - 4;
    }
    if (prec) prec.addEventListener('click', function () { piste.scrollBy({ left: -pas(), behavior: 'smooth' }); });
    if (suiv) suiv.addEventListener('click', function () { piste.scrollBy({ left: pas(), behavior: 'smooth' }); });
    piste.addEventListener('scroll', majBoutons, { passive: true });
    window.addEventListener('resize', majBoutons);
    majBoutons();
  });
}

/* ------------------------------------------------- LIEN « RETOUR EN HAUT » */
function initRetourHaut() {
  $$('[data-retour-haut]').forEach(function (lien) {
    lien.addEventListener('click', function (e) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: prefersReducedMotion() ? 'auto' : 'smooth' });
      const cible = $('#haut');
      if (cible) cible.focus({ preventScroll: true });
    });
  });
}

/* --------------------------------------------- LIEN ACTIF DANS LA NAVIGATION */
function initNavActive() {
  const page = (window.location.pathname.split('/').pop() || 'index.html').toLowerCase();
  $$('.nav-lien[data-page]').forEach(function (lien) {
    const cible = (lien.getAttribute('data-page') || '').toLowerCase();
    if (cible === page || (page === '' && cible === 'index.html')) {
      lien.setAttribute('aria-current', 'page');
    }
  });
}

/* ------------------------------------------------- ANNÉE DE COPYRIGHT */
function initAnnee() {
  $$('[data-annee]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
}

/* --------------------------------------------- COMPTEUR DU PANIER (démo) */
function initCompteurs() {
  const panier = $('[data-compteur-panier]');
  if (panier) panier.textContent = '0';
  const compte = $('[data-compteur-compte]');
  if (compte) compte.textContent = '0';
}

/* ------------------------------------------------------ INITIALISATION */
/* Détection d'un pointeur fin (souris) : permet de n'appliquer le
   « masquage au survol » que là où il a du sens. Sur tactile, les cinq
   liens restent visibles en permanence sous chaque photo. */
function initPointeur() {
  if (window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    document.body.classList.add('souris');
  }
}

function init() {
  initPointeur();
  appliquerLiensSociaux(document);
  /* les conteneurs sans lien pré-existant reçoivent les cinq icônes */
  $$('.socials').forEach(function (c) { if (!c.children.length) construireLiensSociaux(c); });
  initMenuMobile();
  initMenuCategories();
  initRecherche();
  initHeros();
  initRails();
  initRetourHaut();
  initNavActive();
  initAnnee();
  initCompteurs();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
