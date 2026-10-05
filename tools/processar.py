"""Gera as imagens do site a partir de conteudo/ (o que o painel /admin edita):
- cada foto de conteudo/trabalhos.json e dos estilos da home → assets/obras/<nome>.webp (inteira, até 1600 px)
  e assets/obras/<nome>-t.webp (recorte 4:5, 800x1000)
- a foto da abertura → assets/img/abertura-<hash>.webp (recorte 3:4)
- assets/js/obras.js com a lista dos trabalhos, na ordem do painel
Os nomes gerados levam um pedaço do hash da foto: foto igual = nome igual, então só converte o que é novo
ou mudou (mesmo que ela troque a foto mantendo o nome) e apaga o que não é mais usado.
Uso: python tools/processar.py"""
import hashlib, json, pathlib, re, unicodedata
from PIL import Image, ImageOps

RAIZ = pathlib.Path(__file__).resolve().parents[1]
CONTEUDO = RAIZ / "conteudo"
OBRAS = RAIZ / "assets" / "obras"
ESTILOS = {"fineline", "ornamental", "escrita"}


def ler(nome):
    return json.loads((CONTEUDO / f"{nome}.json").read_text(encoding="utf-8"))


def caminho(valor):
    """'/conteudo/fotos/x.webp' (como o painel salva) → arquivo no repositório"""
    return RAIZ / valor.lstrip("/")


def resumo(arq):
    return hashlib.sha1(arq.read_bytes()).hexdigest()[:8]


def nome_de(arq):
    s = unicodedata.normalize("NFKD", arq.stem).encode("ascii", "ignore").decode().lower()
    return (re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "foto") + "-" + resumo(arq)


def abrir(origem):
    return ImageOps.exif_transpose(Image.open(origem)).convert("RGB")


def obra(origem):
    nome = nome_de(origem)
    inteira, recorte = OBRAS / f"{nome}.webp", OBRAS / f"{nome}-t.webp"
    if not (inteira.exists() and recorte.exists()):
        im = abrir(origem)
        im.thumbnail((1600, 1600), Image.LANCZOS)
        im.save(inteira, quality=84, method=4)
        w = im.width
        alvo = (800, 1000) if w >= 800 else (w, int(w * 1.25))
        ImageOps.fit(im, alvo, Image.LANCZOS, centering=(.5, .45)).save(recorte, quality=80, method=4)
        print("  convertida", origem.name)
    return nome


def main():
    OBRAS.mkdir(parents=True, exist_ok=True)
    usados, lista = set(), []
    for t in ler("trabalhos")["trabalhos"]:
        if not t.get("foto"):
            continue
        nome = obra(caminho(t["foto"]))
        usados.add(nome)
        estilo = t.get("estilo") if t.get("estilo") in ESTILOS else "fineline"
        lista.append({"slug": nome, "titulo": (t.get("titulo") or "").strip() or "Tattoo", "estilo": estilo})

    inicio = ler("inicio")
    for chave in ("fineline", "ornamental"):
        foto = inicio["estilos"][chave].get("foto")
        if foto:
            usados.add(obra(caminho(foto)))

    origem = caminho(inicio["abertura"]["foto"])
    saida = RAIZ / "assets" / "img" / f"abertura-{resumo(origem)}.webp"
    for velha in saida.parent.glob("abertura-*.webp"):
        if velha != saida:
            velha.unlink()
    if not saida.exists():
        ImageOps.fit(abrir(origem), (810, 1080), Image.LANCZOS, centering=(.5, .3)).save(saida, quality=86, method=4)
        print("  convertida a foto da abertura")

    for f in OBRAS.glob("*.webp"):
        if f.stem.removesuffix("-t") not in usados:
            f.unlink()

    js = "// gerado por tools/processar.py a partir de conteudo/trabalhos.json — não editar à mão\nwindow.OBRAS = " + json.dumps(lista, ensure_ascii=False, indent=1) + ";\n"
    (RAIZ / "assets" / "js" / "obras.js").write_text(js, encoding="utf-8")
    print(len(lista), "trabalhos")


if __name__ == "__main__":
    main()
