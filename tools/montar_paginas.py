"""Monta as páginas da raiz a partir de tools/modelos/*.html (Jinja) + os textos de conteudo/*.json,
que são o que o painel /admin edita. Rodar depois do processar.py (os nomes das fotos vêm dele).
Uso: python tools/montar_paginas.py"""
import json, pathlib, sys, urllib.parse
from jinja2 import Environment, FileSystemLoader, StrictUndefined

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from processar import nome_de, caminho, resumo  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parents[1]
V = 4  # subir a cada mudança de CSS/JS
BASE_404 = "/agatha-amorim/"  # o 404 do Pages abre em qualquer caminho; trocar para "/" quando tiver domínio
MENU = [("trabalhos.html", "Trabalhos"), ("ritual.html", "O Ritual"), ("cuidados.html", "Cuidados"), ("agendar.html", "Agendar")]


def ler(nome):
    return json.loads((RAIZ / "conteudo" / f"{nome}.json").read_text(encoding="utf-8"))


def main():
    env = Environment(loader=FileSystemLoader(RAIZ / "tools" / "modelos"), autoescape=True,
                      undefined=StrictUndefined, keep_trailing_newline=True)
    env.filters["wa"] = lambda numero: f"https://wa.me/{''.join(c for c in numero if c.isdigit())}"
    env.filters["obra"] = lambda foto: f"assets/obras/{nome_de(caminho(foto))}-t.webp"
    env.filters["abertura"] = lambda foto: f"assets/img/abertura-{resumo(caminho(foto))}.webp"
    contato = ler("contato")
    dados = {
        "V": V, "MENU": MENU, "BASE_404": BASE_404, "ativo": "", "grade": False, "base_href": "",
        "contato": contato, "inicio": ler("inicio"), "ritual": ler("ritual"), "cuidados": ler("cuidados"),
        "mapa": urllib.parse.quote(f"{contato['endereco']}, {contato['complemento'].split('·')[-1].strip()}"),
    }
    for modelo in sorted((RAIZ / "tools" / "modelos").glob("*.html")):
        if modelo.name == "base.html":
            continue
        html = env.get_template(modelo.name).render(**dados)
        (RAIZ / modelo.name).write_text(html, encoding="utf-8")
        print("ok", modelo.name)


if __name__ == "__main__":
    main()
