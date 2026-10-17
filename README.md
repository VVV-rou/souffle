# Souffle de Glace

Application web de respiration Wim Hof (PWA, hors ligne). La référence du projet
est [`SPEC.md`](SPEC.md).

En ligne : https://vvv-rou.github.io/souffle/

## Ajouter des sons

1. Dépose les fichiers dans `sons/respiration/`, `sons/apnee/`, `sons/voix/`,
   `sons/souffle/` (chaque dossier a un README qui dit quels noms sont attendus).
2. Commit + push sur `main`.

Le déploiement liste automatiquement les sons (`sons/sons.json`) et publie le
site. À la prochaine ouverture, l'app télécharge les nouveaux sons pour le hors
ligne.

Une fois le souffle enregistré, reporte les périodes mesurées dans `index.html`,
constante `TEMPOS`.

## Tester en local

```sh
python3 outils/sons.py          # génère sons/sons.json
python3 -m http.server 8000     # puis http://localhost:8000
```

## Installer sur l'iPhone

Safari → l'adresse ci-dessus → Partager → « Sur l'écran d'accueil ».
L'app s'ouvre alors en plein écran avec son icône.

Rappel quotidien : voir `SPEC.md` §7 (automatisation dans Raccourcis).

## Fichiers

- `index.html` — l'application entière (page unique)
- `sw.js` — service worker : cache du code et des sons
- `manifest.webmanifest`, `icones/` — installation PWA (`outils/icones.py` régénère les icônes)
- `reglages.json` — préréglages par défaut, versionnés ; chaque appareil garde ensuite les siens
- `.github/workflows/pages.yml` — déploiement GitHub Pages
