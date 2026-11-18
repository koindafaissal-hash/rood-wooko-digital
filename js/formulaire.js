/* =============================================================================
   ROOD-WOOKO DIGITAL — js/formulaire.js
   Validation du formulaire de contact (JavaScript vanilla) et envoi.
   -----------------------------------------------------------------------------
   Le formulaire n'utilise aucun service tiers : la validation est faite dans
   le navigateur, puis le message est transmis soit via WhatsApp, soit via la
   messagerie du poste de travail.
   ========================================================================== */

/* Numéro WhatsApp de la maison : donnée réelle, à ne pas modifier. */
const RWD_WHATSAPP_CONTACT = '22656433122';
/* Adresse de réception des demandes par e-mail. */
const RWD_EMAIL_CONTACT = 'contact@rood-wooko.bf';

const REGLES = {
  nom:      { requis: true,  min: 2,  message: 'Merci d’indiquer votre nom.' },
  societe:  { requis: false, min: 0,  message: '' },
  email:    { requis: true,  min: 5,  message: 'Merci d’indiquer une adresse e-mail valide.',
              motif: /^[^@\s]+@[^@\s]+\.[a-z]{2,}$/i },
  telephone:{ requis: true,  min: 6,  message: 'Merci d’indiquer un numéro de téléphone.',
              motif: /^[+0-9][0-9 .()\-]{5,}$/ },
  sujet:    { requis: true,  min: 1,  message: 'Merci de choisir un objet.' },
  message:  { requis: true,  min: 10, message: 'Merci d’écrire quelques mots sur votre besoin.' }
};

function valeur(champ) {
  const el = document.getElementById(champ);
  return el ? el.value.trim() : '';
}

function erreur(champ, texte) {
  const bloc = document.getElementById('champ-' + champ);
  if (!bloc) return;
  bloc.classList.add('invalide');
  const message = bloc.querySelector('.champ-erreur');
  if (message && texte) message.textContent = texte;
}

function effacerErreurs() {
  document.querySelectorAll('#formulaire-contact .champ').forEach(function (bloc) {
    bloc.classList.remove('invalide');
  });
}

function valider(champ) {
  const regle = REGLES[champ];
  if (!regle) return true;
  const bloc = document.getElementById('champ-' + champ);
  const v = valeur(champ);
  let valide = true;
  if (regle.requis && v.length === 0) valide = false;
  else if (v.length < regle.min) valide = false;
  else if (regle.motif && !regle.motif.test(v)) valide = false;
  if (!valide) { erreur(champ, regle.message); return false; }
  /* champ valide : on retire le marquage d'erreur */
  if (bloc) bloc.classList.remove('invalide');
  return true;
}

function messageConstruit() {
  return 'Bonjour ' + NOM + ',\n\n' +
         'Nom : ' + valeur('nom') + '\n' +
         (valeur('societe') ? 'Société : ' + valeur('societe') + '\n' : '') +
         'E-mail : ' + valeur('email') + '\n' +
         'Téléphone : ' + valeur('telephone') + '\n' +
         'Objet : ' + valeur('sujet') + '\n\n' +
         valeur('message') + '\n\n' +
         'Envoyé depuis le site web ROOD-WOOKO DIGITAL.';
}

function afficherSucces(texte) {
  const bloc = document.getElementById('message-ok');
  if (!bloc) return;
  bloc.textContent = texte;
  bloc.setAttribute('data-visible', 'true');
}

function initFormulaire() {
  const formulaire = document.getElementById('formulaire-contact');
  if (!formulaire) return;

  /* validation à la volée, dès la sortie d'un champ */
  Object.keys(REGLES).forEach(function (champ) {
    const el = document.getElementById(champ);
    if (!el) return;
    el.addEventListener('blur', function () {
      const bloc = document.getElementById('champ-' + champ);
      if (bloc.classList.contains('invalide')) valider(champ);
    });
    el.addEventListener('input', function () {
      const bloc = document.getElementById('champ-' + champ);
      if (bloc.classList.contains('invalide')) valider(champ);
    });
  });

  function controler() {
    effacerErreurs();
    let valide = true;
    Object.keys(REGLES).forEach(function (champ) {
      if (!valider(champ)) valide = false;
    });
    return valide;
  }

  /* envoi par WhatsApp */
  formulaire.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!controler()) {
      const premier = formulaire.querySelector('.champ.invalide input, .champ.invalide select, .champ.invalide textarea');
      if (premier) premier.focus();
      return;
    }
    const lien = 'https://wa.me/' + RWD_WHATSAPP_CONTACT + '?text=' + encodeURIComponent(messageConstruit());
    afficherSucces('Votre message est prêt. Nous ouvrons WhatsApp avec le récapitulatif de votre demande — si rien ne se passe, écrivez-nous au +226 56 43 31 22.');
    window.open(lien, '_blank', 'noopener');
  });

  /* envoi par messagerie */
  const boutonEmail = document.getElementById('envoi-email');
  if (boutonEmail) {
    boutonEmail.addEventListener('click', function () {
      if (!controler()) {
        const premier = formulaire.querySelector('.champ.invalide input, .champ.invalide select, .champ.invalide textarea');
        if (premier) premier.focus();
        return;
      }
      const sujet = 'Demande depuis le site — ' + valeur('sujet');
      const corps = messageConstruit();
      const lien = 'mailto:' + RWD_EMAIL_CONTACT + '?subject=' + encodeURIComponent(sujet) + '&body=' + encodeURIComponent(corps);
      afficherSucces('Votre messagerie s’ouvre avec le message pré-rempli. Si elle ne s’ouvre pas, écrivez directement à ' + RWD_EMAIL_CONTACT + '.');
      window.location.href = lien;
    });
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initFormulaire);
} else {
  initFormulaire();
}
