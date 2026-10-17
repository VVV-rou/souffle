# Annonces de phase (voix de Val)

Un fichier par annonce. **Le nom du fichier compte** (sans accent, minuscules) ;
l'extension est libre (`.mp3`, `.m4a`, `.wav`).

| Fichier          | Ce qui est dit         | Quand                                  |
|------------------|------------------------|----------------------------------------|
| `trois.mp3`      | trois                  | 3e respiration avant la fin du cycle   |
| `deux.mp3`       | deux                   | 2e avant la fin                        |
| `une.mp3`        | une                    | dernière respiration                   |
| `parti.mp3`      | c'est parti            | première respiration de la séance      |
| `retention.mp3`  | rétention              | entrée en apnée poumons vides          |
| `inspire.mp3`    | inspire, et retiens    | sortie d'apnée                         |
| `relache.mp3`    | relâche                | entrée en reprise                      |
| `repart.mp3`     | on repart              | retour aux respirations                |
| `termine.mp3`    | c'est terminé          | fin de séance                          |

`trois`, `deux`, `une` servent aussi au décompte de la fin de la préparation.

Traitement : découpage serré (pas de silence en tête), normalisation, fondus
courts d'entrée et de sortie. Un fichier manquant est simplement ignoré.
