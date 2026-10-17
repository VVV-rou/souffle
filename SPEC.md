# Souffle de Glace — spécification

Application web de respiration Wim Hof, personnelle, pour Val (iPhone + MacBook).
Dépôt : `VVV-rou/souffle`. Hébergement visé : GitHub Pages, puis éventuellement
un sous-domaine de `valentinrouanet.fr`.

Ce fichier est la référence du projet. Il remplace l'historique de la conversation
où l'application a été conçue (six versions successives en artefact Claude).

---

## 1. Pourquoi on quitte l'artefact Claude

L'application existe déjà sous forme d'artefact (six versions, fonctionnelle).
Trois limites ont motivé le passage à un hébergement propre :

- **Les sons.** Le magasin de fichiers d'un artefact n'accepte aucun type audio.
  Contournement actuel : encoder les MP3 en base64 dans un fichier texte, plafond
  de ~15 Mo par morceau. Dans un dépôt, un MP3 est un MP3.
- **L'icône et le plein écran.** La page tourne dans un cadre embarqué, donc iOS
  prend l'icône et le titre du document parent (claude.ai). Hébergée en propre,
  la page est au premier plan : manifeste PWA + `apple-touch-icon` donnent l'icône
  **et** le plein écran sans barre Safari.
- **Le hors ligne.** Un service worker permet une séance sans réseau.

Ce qu'on perd : la synchronisation automatique des réglages entre appareils
(elle reposait sur le stockage serveur de l'artefact). Compensation prévue :
un fichier de préréglages versionné dans le dépôt + `localStorage` par appareil.

---

## 2. Structure du dépôt

```
index.html            page unique
app.js, style.css     si on sépare ; sinon tout en ligne dans index.html
manifest.webmanifest  nom, icônes, display: standalone, theme/background color
sw.js                 service worker : cache code + sons
icones/               192, 512, 1024 px + apple-touch-icon
sons/
  respiration/        banque « respirations » — tirage aléatoire
  apnee/              banque « apnées » — tirage aléatoire
  voix/               annonces de phase (voix de Val)
  souffle/            souffle de guidage (voix de Val), 3 tempos
SPEC.md               ce fichier
```

---

## 3. Déroulé d'une séance

```
Préparation → [ Respirations → Rétention poumons vides → Inspiration
             → Rétention poumons pleins → Reprise ] × N cycles → Bilan
```

La reprise est sautée après le dernier cycle.

| Phase | Comportement | Réglable |
|---|---|---|
| Préparation | Compte à rebours avant la 1re respiration | Durée |
| Respirations | N respirations guidées au tempo choisi | Nombre, tempo |
| Rétention poumons vides | Chronomètre qui monte. **Toujours libre** : on passe par appui écran. Jamais minutée. | Rien |
| Inspiration | Grande inspiration guidée (~2,3 s) | Rien |
| Rétention poumons pleins | Minutée **ou** libre (appui écran) | Mode + durée |
| Reprise | Respirations libres entre deux cycles. Minutée, libre (appui écran) ou aucune | Mode + durée |
| Bilan | Temps de rétention par cycle, moyenne, comparaison au record | — |

**Horloge.** Tout le séquencement est calé sur `AudioContext.currentTime`, jamais
sur `setTimeout`, pour éviter toute dérive sur 40 respirations. Les sons sont
programmés en avance (fenêtre ~1,2 s) sur cette même horloge.

---

## 4. Interface

### Encadré « Séance »
- Cycles (pas de 1)
- Respirations par cycle
- Durée de préparation
- **Rythme** : choix fixe **Lent / Standard / Rapide** — déplacé ici depuis
  l'ancien encadré « Rythme respiratoire », qui disparaît.

Plus de réglage en secondes, plus de curseur de ratio inspiration/expiration.
Les trois tempos sont ceux des enregistrements de souffle (voir §5).

### Encadré « Rétentions »
- Poumons vides : aucun réglage (toujours libre).
- Récupération : Minutée / Libre + durée.
- Reprise entre les cycles : Libre / Minutée / Aucune + durée.

### Encadré « Son »
- Volume d'ambiance
- Durée du fondu enchaîné
- Volume du guidage

Voix et souffle sont intégrés au dépôt, non modifiables depuis l'application.

**Musiques : importées sur l'appareil** (révision du 17 oct. 2026). Les morceaux
choisis sont protégés par le droit d'auteur ; le dépôt et le site étant publics,
ils ne sont pas versionnés. L'encadré Son a une section par banque (respirations,
apnées) : import depuis Fichiers, déplacement d'une banque à l'autre, retrait.
Stockage IndexedDB, une fois par appareil, conservé et disponible hors ligne.
Sur iPhone, l'app installée a son propre stockage, séparé de Safari.

### Encadré « Repères »
- Garder l'écran allumé (Wake Lock)
- Décompte des 3 dernières respirations (voir §6)

### Écran de séance
- Orbe centrale qui se dilate et se contracte au rythme
- Couleur par phase : cyan (respirations) → indigo (rétention) → ambre
  (récupération) → vert sauge (reprise)
- Compteur de respirations, chronomètre de rétention
- Toute la surface est une zone d'appui pendant les phases libres

### Calendrier (nouveau)
Grille du mois en cours, jours pratiqués marqués. Navigation mois précédent /
suivant. But : voir d'un coup d'œil les trous et la régularité. Les séances sont
déjà horodatées dans l'historique.

---

## 5. Audio

### Deux banques, tirage aléatoire (révisé le 17 oct. 2026)
- Zone **respirations** (préparation + respirations) : banque respirations.
- Zone **apnée** (poumons vides, inspiration, poumons pleins, reprise — jusqu'au
  retour des respirations) : banque apnées.
- À chaque changement de zone : un morceau tiré au hasard, **joué depuis le
  début**, jamais le dernier joué de cette banque ; fondu croisé ~2,6 s.
- Si un morceau se termine avant la fin de la zone : un autre morceau de la même
  banque, au hasard, enchaîné avec le fondu réglé dans l'application.
- Sans morceau dans une banque, l'autre la remplace.

### Guidage : souffle enregistré
Plus aucune synthèse. Le souffle de guidage est la voix de Val, enregistrée à
trois tempos correspondant à Lent / Standard / Rapide. **Les périodes réelles
des trois tempos seront mesurées sur les enregistrements** et codées en dur :
aucun étirement, donc aucun décalage de hauteur.

Protocole d'enregistrement retenu :
- Suivre l'application Wim Hof officielle, **au casque**, sur chacun des trois
  réglages, et respirer en même temps.
- Six à huit respirations d'affilée par tempo, en continu (le découpage est fait
  après coup, ce qui permet de choisir la plus propre).
- MKE 600 + Zoom F3, mono, 48 kHz, 32 bits flottant.

### Annonces de phase : voix enregistrée
Mots à enregistrer, prise séparée, ton de séance (voix proche, posée, basse) :

> trois — deux — une — rétention — inspire, et retiens — relâche — on repart — c'est terminé

Correspondance :
- `trois` / `deux` / `une` → décompte des 3 dernières respirations
- `rétention` → entrée en apnée poumons vides
- `inspire, et retiens` → sortie d'apnée
- `relâche` → entrée en reprise
- `on repart` → retour aux respirations
- `c'est terminé` → fin de séance

Traitement : découpage, normalisation, fondus d'entrée et de sortie. Les fichiers
ne sont pas transformés au-delà de ça.

### Supprimés
Synthèse du souffle, bol tibétain, motifs de notes, synthèse vocale du système,
réglage « grain du souffle », choix du type de guidage.

---

## 6. Décompte des 3 dernières respirations

Trois canaux simultanés :
1. Les 3 derniers segments de la barre de progression sont teintés en indigo dès
   le début du cycle — la fin se voit venir de loin.
2. Le grand chiffre bascule de « 27 / 30 » à « 3 », « 2 », « 1 » avec la mention
   « avant rétention ».
3. L'écran vire progressivement du cyan vers l'indigo de rétention (25 %, 55 %,
   85 %), et la voix annonce trois / deux / une.

---

## 7. Rappels quotidiens — limite connue

Une application web **ne peut pas** programmer une notification pour plus tard :
l'API de notifications ne se déclenche que pendant que la page tourne, et les
notifications poussées sur iPhone exigent un serveur. Un site statique ne peut
pas le faire.

Solution retenue, à configurer une fois sur l'iPhone : une automatisation
personnelle dans **Raccourcis** — « Tous les jours à 8h00 → Ouvrir l'app →
Souffle », avec « Exécuter sans confirmation » activé. Ça ouvre l'application
plutôt que d'afficher une notification.

Même remarque pour l'icône de l'écran d'accueil si l'app n'est pas installée en
PWA : un raccourci « Ouvrir l'URL » permet de choisir une icône personnalisée,
au prix du plein écran. Avec le manifeste PWA correctement servi, ce compromis
disparaît.

---

## 8. Persistance

- Réglages et historique : `localStorage`, par appareil.
- Toujours envelopper lecture et écriture dans `try/catch` : le stockage peut
  être bloqué ou vide.
- Historique : date + durées de rétention par cycle, 30 dernières séances.
  C'est la source du calendrier et du record.

---

## 9. État au moment d'écrire

- Dépôt `VVV-rou/souffle` créé, public, vide.
- Enregistrements voix et souffle : à faire par Val.
- Musiques : à fournir par Val, réparties entre les deux banques.
- Version artefact existante : fonctionnelle, sert de référence de comportement
  (machine à états, moteur audio deux platines, décompte, calendrier à ajouter).
