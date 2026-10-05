"""Gera assets/obras (-t = recorte 4:5, sem sufixo = inteira) e assets/js/obras.js a partir da lista OBRAS.
Lê os originais de ../_ref/ig (prints de 640 px do Instagram; trocar pelos originais dela quando vierem).
Uso: python tools/processar.py"""
import json, pathlib
from PIL import Image, ImageOps

RAIZ = pathlib.Path(__file__).resolve().parents[1]
ORIG = RAIZ.parent / "_ref" / "ig"
SAIDA = RAIZ / "assets" / "obras"

# slug, título, estilo (fineline | ornamental) — a classificação é minha, CONFIRMAR com ela
OBRAS = [
    ("sol-juliana", "Sol ornamental", "ornamental"),
    ("fechamento-ju", "Fechamento com espelho e ramos", "ornamental"),
    ("ornamental-suellen", "Ornamental no antebraço e mão", "ornamental"),
    ("primeira-barbara", "Floral na coluna", "fineline"),
    ("onca", "Onça com sol", "fineline"),
    ("borboleta-andressa", "Borboleta", "fineline"),
    ("homenagem-claudia", "Homenagem com música", "fineline"),
    ("homenagens-gabi", "Homenagens aos pets", "fineline"),
    ("homenagem-leandro", "Retrato em traço", "fineline"),
    ("escritas-thalita", "Escrita delicada", "fineline"),
]

def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    lista = []
    for slug, titulo, estilo in OBRAS:
        im = Image.open(ORIG / f"{slug}.jpg").convert("RGB")
        im.thumbnail((1600, 1600))
        im.save(SAIDA / f"{slug}.webp", quality=86, method=6)
        w, h = im.size
        t = ImageOps.fit(im, (min(w, int(h * .8)), min(h, int(w * 1.25))), centering=(.5, .45))
        t.save(SAIDA / f"{slug}-t.webp", quality=84, method=6)
        lista.append({"slug": slug, "titulo": titulo, "estilo": estilo, "w": t.width, "h": t.height})
        print("ok", slug, im.size, t.size)
    js = "// gerado por tools/processar.py — não editar à mão\nwindow.OBRAS = " + json.dumps(lista, ensure_ascii=False, indent=1) + ";\n"
    (RAIZ / "assets" / "js" / "obras.js").write_text(js, encoding="utf-8")

if __name__ == "__main__":
    main()
