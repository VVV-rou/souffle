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

## Mesure des périodes

Une fois découpées, mesure dans Resolve ou Audacity :

- la **période** : durée totale du fichier ;
- l'**inspiration** : du début jusqu'au moment où l'expiration commence.

Puis reporte les deux valeurs dans `index.html`, constante `TEMPOS`
(cherche « valeurs mesurées »). L'orbe et le compteur suivent ces valeurs.
