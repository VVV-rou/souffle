# Souffle de guidage (voix de Val)

Une seule respiration complète (inspiration + expiration) par tempo, joués en
boucle au début de chaque respiration. **Le nom du fichier compte** :

| Fichier         | Tempo    |
|-----------------|----------|
| `lent.mp3`      | Lent     |
| `standard.mp3`  | Standard |
| `rapide.mp3`    | Rapide   |

Extension libre (`.mp3`, `.m4a`, `.wav`).

## Découpage

Le fichier commence **pile au début de l'inspiration** (aucun silence en tête)
et dure exactement une période : inspiration + expiration, jusqu'au début de
l'inspiration suivante. Aucun étirement n'est appliqué.

## Mesures actuelles

| Tempo    | Période | Inspiration | Source                                |
|----------|---------|-------------|---------------------------------------|
| Lent     | 5,014 s | 2,238 s     | `Repi_Lent.WAV`, 21,132 → 26,146 s    |
| Standard | 3,484 s | 1,706 s     | `Respi_moyen.WAV`, 4,284 → 7,768 s    |
| Rapide   | 2,800 s | 1,392 s     | `Respi_rapide.WAV`, 16,638 → 19,438 s |

Prises MKE 600 + Zoom F3, 96 kHz 32 bits flottant, coupe de 50 Hz, normalisées
à −24 dBFS RMS, fondus de 6 ms / 25 ms, MP3 160 kb/s 48 kHz.

## Si tu réenregistres

Une fois découpées, mesure dans Resolve ou Audacity :

- la **période** : durée totale du fichier ;
- l'**inspiration** : du début jusqu'au moment où l'expiration commence.

Puis reporte les deux valeurs dans `index.html`, constante `TEMPOS`
(cherche « valeurs mesurées »). L'orbe et le compteur suivent ces valeurs.
