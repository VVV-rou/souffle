"""Liste les sons du dépôt dans sons/sons.json.

GitHub Pages ne liste pas le contenu des dossiers : l'application lit donc ce
fichier pour savoir quels morceaux existent. Le workflow de déploiement le
régénère à chaque push ; en local, lance simplement :

    python3 outils/sons.py
"""
import json
import unicodedata
from pathlib import Path
from urllib.parse import quote

RACINE = Path(__file__).resolve().parent.parent
SONS = RACINE / "sons"
EXT = {".mp3", ".m4a", ".aac", ".wav", ".aif", ".aiff", ".caf", ".flac", ".mp4"}
VOIX = ["trois", "deux", "une", "retention", "inspire", "relache", "repart", "termine"]
TEMPOS = ["lent", "standard", "rapide", "inspiration", "expiration"]


def fichiers(dossier: str):
    d = SONS / dossier
    if not d.is_dir():
        return []
    return sorted(
        (f for f in d.iterdir() if f.is_file() and f.suffix.lower() in EXT and not f.name.startswith(".")),
        key=lambda f: f.name.lower(),
    )


def url(f: Path) -> str:
    rel = f.relative_to(RACINE).as_posix()
    return quote(unicodedata.normalize("NFC", rel))


def cle(f: Path) -> str:
    """Nom sans extension, minuscules, sans accents : « Rétention.mp3 » → « retention »."""
    nom = unicodedata.normalize("NFD", f.stem.lower())
    return "".join(c for c in nom if not unicodedata.combining(c)).strip()


def par_nom(dossier: str, attendus):
    res, inconnus = {}, []
    for f in fichiers(dossier):
        k = cle(f)
        if k in attendus and k not in res:
            res[k] = url(f)
        else:
            inconnus.append(f.name)
    manquants = [k for k in attendus if k not in res]
    if manquants:
        print(f"  {dossier}/ : manquant(s) → {', '.join(manquants)}")
    if inconnus:
        print(f"  {dossier}/ : ignoré(s), nom non reconnu → {', '.join(inconnus)}")
    return res


def main():
    liste = {
        "respiration": [url(f) for f in fichiers("respiration")],
        "apnee": [url(f) for f in fichiers("apnee")],
        "voix": par_nom("voix", VOIX),
        "souffle": par_nom("souffle", TEMPOS),
    }
    (SONS / "sons.json").write_text(json.dumps(liste, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"sons/sons.json : {len(liste['respiration'])} respiration(s), {len(liste['apnee'])} apnée(s), "
        f"{len(liste['voix'])}/{len(VOIX)} voix, {len(liste['souffle'])}/{len(TEMPOS)} souffles"
    )


if __name__ == "__main__":
    main()
