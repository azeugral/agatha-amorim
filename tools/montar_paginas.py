"""Monta as páginas da raiz a partir de tools/paginas/*.html (só o <main>) + cabeçalho e rodapé comuns.
Cada arquivo começa com 3 linhas:  título | descrição | item do menu ativo (ou -)
Uso: python tools/montar_paginas.py"""
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[1]
V = 3  # subir a cada deploy que mude CSS/JS
ATUAL = ' aria-current="page"'
MENU = [("trabalhos.html", "Trabalhos"), ("ritual.html", "O Ritual"), ("cuidados.html", "Cuidados"), ("agendar.html", "Agendar")]

CABECA = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{titulo}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#f4ede4">
<meta property="og:type" content="website">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="assets/img/og.jpg">
<link rel="icon" href="favicon.ico" sizes="48x48">
<link rel="icon" href="assets/img/favicon-192.png" type="image/png" sizes="192x192">
<link rel="icon" href="assets/img/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,400;0,500;1,400&family=Marcellus&display=swap">
<link rel="stylesheet" href="assets/css/estilo.css?v={v}">
</head>
<body>
<a class="pular" href="#conteudo">Pular para o conteúdo</a>
<header class="topo">
  <div class="wrap topo__in">
    <a class="marca" href="index.html" aria-label="Agatha Amorim Tattoo Studio, início"><img src="assets/img/logo.webp?v={v}" alt="Agatha Amorim Tattoo Studio" width="1400" height="458"></a>
    <button class="menu-btn" aria-expanded="false" aria-controls="menu" aria-label="Abrir menu"><span></span><span></span></button>
    <nav id="menu" class="nav" aria-label="Principal"><ul class="menu">{menu}</ul></nav>
  </div>
</header>
<main id="conteudo">
"""

RODAPE = """</main>
<footer class="rodape">
  <div class="wrap">
    <div class="rodape__in">
      <div class="rodape__marca">
        <a class="marca" href="index.html"><img src="assets/img/logo-branco.webp?v={v}" alt="Agatha Amorim Tattoo Studio" width="1400" height="458" loading="lazy"></a>
        <p>Fine line e ornamental, com hora marcada, em estúdio privado no Centro de Diadema.</p>
      </div>
      <div>
        <h4>Páginas</h4>
        <ul><li><a href="index.html">Início</a></li>{paginas}</ul>
      </div>
      <div>
        <h4>Contato</h4>
        <ul>
          <li><a href="https://wa.me/5511994024060" target="_blank" rel="noopener">WhatsApp</a></li>
          <li><a href="https://www.instagram.com/agathaamorim.tattoo/" target="_blank" rel="noopener">Instagram</a></li>
          <li>Rua Arthur Sampaio Moreira, 115, sala 5, 3º andar · Centro, Diadema</li>
        </ul>
      </div>
    </div>
    <div class="rodape__fim">
      <span>© <span data-ano>2026</span> Agatha Amorim Tattoo Studio</span>
      <span>Site por <a href="https://lrgz.com.br" target="_blank" rel="noopener">L R G Z</a></span>
    </div>
  </div>
</footer>
{scripts}<script src="assets/js/main.js?v={v}" defer></script>
</body>
</html>
"""


def main():
    for f in sorted((RAIZ / "tools" / "paginas").glob("*.html")):
        linhas = f.read_text(encoding="utf-8").split("\n")
        titulo, desc, ativo = (l.strip() for l in linhas[:3])
        corpo = "\n".join(linhas[3:])
        menu = "".join(f'<li><a href="{h}"{ATUAL if h == ativo else ""}>{n}</a></li>' for h, n in MENU)
        paginas = "".join(f'<li><a href="{h}">{n}</a></li>' for h, n in MENU)
        scripts = f'<script src="assets/js/obras.js?v={V}" defer></script>\n' if "data-grade" in corpo else ""
        # o 404 do Pages abre em qualquer caminho: fixa a base (trocar para "/" quando tiver domínio)
        cabeca = CABECA.replace("<head>\n", '<head>\n<base href="/agatha-amorim/">\n') if f.name == "404.html" else CABECA
        html = cabeca.format(titulo=titulo, desc=desc, menu=menu, v=V) + corpo.rstrip() + "\n" + RODAPE.format(paginas=paginas, scripts=scripts, v=V)
        (RAIZ / f.name).write_text(html, encoding="utf-8")
        print("ok", f.name)


if __name__ == "__main__":
    main()
