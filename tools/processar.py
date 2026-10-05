"""Gera assets/obras (-t = recorte 4:5 800x1000, sem sufixo = inteira até 1600 px) e assets/js/obras.js a partir de OBRAS.
Originais: ../_ref/ig (posts recentes, prints de 640 px) e ../_ref/zip/Agatha (zip do cliente, pelo prefixo do nome).
A ordem da lista é a ordem do site: mais recentes primeiro.
Uso: python tools/processar.py"""
import json, pathlib
from PIL import Image, ImageOps

RAIZ = pathlib.Path(__file__).resolve().parents[1]
IG = RAIZ.parent / "_ref" / "ig"
ZIP = RAIZ.parent / "_ref" / "zip" / "Agatha"
SAIDA = RAIZ / "assets" / "obras"

# slug, título, estilo (fineline | ornamental | escrita), origem ("ig:<arquivo>" ou prefixo do arquivo do zip)
# a classificação e os títulos são meus — CONFIRMAR com ela
OBRAS = [
    ("sol-ornamental", "Sol ornamental", "ornamental", "ig:sol-juliana"),
    ("fechamento-espelho", "Fechamento com espelho e ramos", "ornamental", "ig:fechamento-ju"),
    ("ornamental-mao", "Ornamental no antebraço e na mão", "ornamental", "ig:ornamental-suellen"),
    ("floral-coluna", "Floral na coluna", "fineline", "ig:primeira-barbara"),
    ("onca-sol", "Onça com sol", "fineline", "ig:onca"),
    ("borboleta-data", "Borboleta e data", "fineline", "ig:borboleta-andressa"),
    ("musica", "Homenagem com música", "fineline", "ig:homenagem-claudia"),
    ("pets-ombro", "Homenagem aos pets", "fineline", "ig:homenagens-gabi"),
    ("retrato-traco", "Retrato em traço", "fineline", "ig:homenagem-leandro"),
    ("escrita-costas", "Escrita nas costas", "escrita", "ig:escritas-thalita"),
    ("peonias-ombro", "Peônias no ombro", "fineline", "658883450"),
    ("escrita-asas", "Escrita com asas", "escrita", "654988765"),
    ("escrita-orelha", "Escrita atrás da orelha", "escrita", "650919478"),
    ("escrita-antebraco", "Escrita no antebraço", "escrita", "650919226"),
    ("molecula", "Molécula", "fineline", "650241373"),
    ("datas", "Datas", "escrita", "649998492"),
    ("lotus", "Lótus ornamental", "ornamental", "649242463"),
    ("floral-ombro", "Floral no ombro", "fineline", "649224177"),
    ("escrita-pe", "Escrita no pé", "escrita", "649071129"),
    ("coracao", "Coração", "fineline", "631965743"),
    ("equilibrio", "Equilíbrio", "escrita", "631502050"),
    ("rosa-mao", "Rosa na mão", "fineline", "631017927"),
    ("coracao-escrita", "Coração e escrita", "escrita", "629943821"),
    ("rosa-preta", "Rosa preta", "fineline", "629143854"),
    ("pet-contorno", "Pet em contorno", "fineline", "628755444"),
    ("escrita-delicada", "Escrita delicada", "escrita", "627989989"),
    ("rosa-nome", "Rosa com nome", "fineline", "626115591"),
    ("medalhao", "Medalhão", "fineline", "625881109"),
    ("rosa-clavicula", "Rosa na clavícula", "fineline", "625315699"),
    ("escrita-coluna", "Escrita na coluna", "escrita", "625197464"),
    ("nome-sol", "Nome com sol", "escrita", "625053641"),
    ("pets-retrato", "Retrato dos pets", "fineline", "624890938"),
    ("pena", "Pena", "fineline", "624707138"),
    ("borboleta-antebraco", "Borboleta", "fineline", "624535927"),
    ("frase-costela", "Frase na costela", "escrita", "624095423"),
    ("lua-mao", "Lua na mão", "fineline", "624057943"),
    ("arvore-vida", "Árvore da vida", "fineline", "623902442"),
    ("frase-costela-2", "Frase na lateral", "escrita", "623820073"),
    ("baleias", "Baleias e ondas", "fineline", "622489999"),
    ("escritas-maos", "Escritas nas mãos", "escrita", "622444322"),
    ("escrita-ombro", "Escrita no ombro", "escrita", "621875385"),
    ("rosa-perna", "Rosa", "fineline", "621670197"),
    ("data-antebraco", "Data", "escrita", "621659683"),
    ("floral-escrita", "Floral e escrita", "fineline", "621597060"),
    ("frase-costas", "Frase nas costas", "escrita", "621465775"),
    ("borboleta-perna", "Borboleta na perna", "fineline", "621404154"),
    ("ano", "Ano", "escrita", "621370151"),
    ("palavra-mao", "Palavra na mão", "escrita", "621253704"),
    ("frase-coluna", "Frase na coluna", "escrita", "620907250"),
    ("palavra-nuca", "Palavra na nuca", "escrita", "620521845"),
    ("rosa-mao-2", "Rosa na mão", "fineline", "620408954"),
    ("borboleta-blackwork", "Borboleta", "fineline", "620367485"),
    ("frase-ombro", "Frase no ombro", "escrita", "619716294"),
    ("simbolo-pescoco", "Símbolo no pescoço", "fineline", "619596614"),
    ("frase-pulso", "Frase no pulso", "escrita", "619471519"),
    ("frase-braco", "Frase no braço", "escrita", "619312843"),
    ("pets-desenho", "Pets em desenho", "fineline", "619176188"),
    ("escrita-rosa", "Escrita e rosa", "escrita", "618570776"),
    ("nome-tornozelo", "Nome no tornozelo", "escrita", "618138640"),
    ("patinha", "Patinha", "fineline", "617249221"),
    ("floral-antebraco", "Floral no antebraço", "fineline", "504469505"),
]


def origem(o):
    if o.startswith("ig:"):
        return IG / f"{o[3:]}.jpg"
    return next(ZIP.glob(f"{o}_*.jpg"))


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    for velho in SAIDA.glob("*.webp"):
        velho.unlink()
    lista = []
    for slug, titulo, estilo, o in OBRAS:
        im = ImageOps.exif_transpose(Image.open(origem(o))).convert("RGB")
        im.thumbnail((1600, 1600), Image.LANCZOS)
        im.save(SAIDA / f"{slug}.webp", quality=84, method=6)
        w, h = im.size
        alvo = (800, 1000) if w >= 800 else (w, int(w * 1.25))
        t = ImageOps.fit(im, alvo, Image.LANCZOS, centering=(.5, .45))
        t.save(SAIDA / f"{slug}-t.webp", quality=80, method=6)
        lista.append({"slug": slug, "titulo": titulo, "estilo": estilo})
    js = "// gerado por tools/processar.py — não editar à mão\nwindow.OBRAS = " + json.dumps(lista, ensure_ascii=False, indent=1) + ";\n"
    (RAIZ / "assets" / "js" / "obras.js").write_text(js, encoding="utf-8")
    print(len(lista), "obras")


if __name__ == "__main__":
    main()
