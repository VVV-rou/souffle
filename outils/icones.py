"""Génère les icônes de l'application dans icones/.

Une orbe cyan sur fond nuit, comme l'écran de séance.
Usage : python3 outils/icones.py   (nécessite Pillow)
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

RACINE = Path(__file__).resolve().parent.parent
SORTIE = RACINE / "icones"
FOND = (7, 12, 17)
CYAN = (87, 199, 220)
INDIGO = (145, 135, 230)


def orbe(taille: int, echelle: float) -> Image.Image:
    """Dessine en 4x puis réduit, pour des bords propres."""
    s = taille * 4
    img = Image.new("RGB", (s, s), FOND)
    c = s / 2
    r = s * 0.5 * echelle

    # halo
    halo = Image.new("L", (s, s), 0)
    ImageDraw.Draw(halo).ellipse([c - r * 1.15, c - r * 1.15, c + r * 1.15, c + r * 1.15], fill=90)
    halo = halo.filter(ImageFilter.GaussianBlur(s * 0.06))
    img.paste(Image.new("RGB", (s, s), CYAN), mask=halo)

    # corps de l'orbe : dégradé radial, plus clair vers le haut
    corps = Image.new("RGB", (s, s), FOND)
    masque = Image.new("L", (s, s), 0)
    d_corps, d_masque = ImageDraw.Draw(corps), ImageDraw.Draw(masque)
    pas = 160
    for i in range(pas, 0, -1):
        k = i / pas                      # 1 au bord, 0 au centre
        rr = r * k
        cy = c - r * 0.16 * (1 - k)      # centre lumineux décalé vers le haut
        t = (1 - k) ** 1.4
        col = tuple(int(FOND[j] * (1 - (0.28 + 0.6 * t)) + CYAN[j] * (0.28 + 0.6 * t)) for j in range(3))
        d_corps.ellipse([c - rr, cy - rr, c + rr, cy + rr], fill=col)
        d_masque.ellipse([c - rr, cy - rr, c + rr, cy + rr], fill=255)
    img.paste(corps, mask=masque)

    # anneau fin
    d = ImageDraw.Draw(img)
    ra = r * 1.22
    d.ellipse([c - ra, c - ra, c + ra, c + ra], outline=tuple(int(FOND[j] * .55 + CYAN[j] * .45) for j in range(3)),
              width=max(2, int(s * 0.006)))
    # point indigo de rétention
    pr = s * 0.022
    d.ellipse([c - pr, c + ra - pr, c + pr, c + ra + pr], fill=INDIGO)

    return img.resize((taille, taille), Image.LANCZOS)


def main():
    SORTIE.mkdir(exist_ok=True)
    for t in (192, 512, 1024):
        orbe(t, 0.56).save(SORTIE / f"icone-{t}.png", optimize=True)
    orbe(180, 0.56).save(SORTIE / "apple-touch-icon.png", optimize=True)
    # zone de sécurité « maskable » : tout tient dans le cercle central de 80 %
    orbe(512, 0.44).save(SORTIE / "icone-maskable-512.png", optimize=True)
    print("icônes écrites dans", SORTIE)


if __name__ == "__main__":
    main()
