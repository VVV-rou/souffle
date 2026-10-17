# Souffle de guidage (voix de Val)

Une seule respiration complète (inspiration + expiration) par tempo, joués en
boucle au début de chaque respiration. **Le nom du fichier compte** :

| Fichier         | Tempo    |
|-----------------|----------|
| `lent.mp3`      | Lent     |
| `standard.mp3`  | Standard |
| `rapide.mp3`    | Rapide   |

Plus deux sons ponctuels, tirés du cycle lent :

| Fichier            | Joué                                                        |
|--------------------|-------------------------------------------------------------|
| `inspiration.mp3`  | début de la rétention poumons pleins, avec « inspire, et retiens » |
| `expiration.mp3`   | début de la reprise, avec « relâche »                       |

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
à −24 dBFS RMS, MP3 160 kb/s 48 kHz. Fondu d'entrée de l'inspiration : 320 ms
(lent), 260 ms (standard), 200 ms (rapide) ; fondu de sortie 25 ms.
`inspiration.mp3` (2,238 s) et `expiration.mp3` (2,776 s) : les deux moitiés du
cycle lent, au même niveau que `lent.mp3`.

## Si tu réenregistres

Une fois découpées, mesure dans Resolve ou Audacity :

- la **période** : durée totale du fichier ;
- l'**inspiration** : du début jusqu'au moment où l'expiration commence.

Puis reporte les deux valeurs dans `index.html`, constante `TEMPOS`
(cherche « valeurs mesurées »). L'orbe et le compteur suivent ces valeurs.
