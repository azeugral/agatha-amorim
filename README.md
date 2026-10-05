# Agatha Amorim Tattoo Studio

Site da tatuadora Agatha Amorim ([@agathaamorim.tattoo](https://www.instagram.com/agathaamorim.tattoo/)), fine line e ornamental, em estúdio privado no Centro de Diadema - SP.
HTML, CSS e JS puros, sem build. Prévia em GitHub Pages, com `noindex` e `robots.txt` bloqueando até ter domínio.

## Estrutura

- `index.html`, `trabalhos.html`, `ritual.html`, `cuidados.html`, `agendar.html`, `404.html`: **gerados**. Editar o `<main>` em `tools/paginas/*.html` e rodar `python tools/montar_paginas.py` (cabeçalho, rodapé e `?v=` vêm de lá).
- `assets/obras/`: tattoos em WebP, `-t` = recorte 4:5, sem sufixo = inteira.
- `assets/js/obras.js`: **gerado** por `python tools/processar.py` a partir da lista `OBRAS` (lê `../_ref/ig`).
- `assets/js/main.js`: `CONFIG.whatsapp`, menu, raios de sol, grade com filtro por hash, imagem ampliada e formulário que monta a mensagem do WhatsApp.
- `tools/gerar_logo.py`: logo em café e em branco (do logo transparente dela), favicon com os raios do sol, apple-touch, `og.jpg` e a foto dela.

A cada deploy que mude CSS/JS, subir `V` em `tools/montar_paginas.py` e remontar.

## Identidade

Tirada dos stories e do logo dela.
- Cores: areia `#f5efe7`, taupe `#b9a088` (stories de cuidados), pêssego `#dda06f` (stories do Ritual e do endereço), café `#342820` no texto.
- Fontes: Marcellus nos títulos e Jost no texto (Italiana e o manuscrito saíram em 05/10: difíceis de ler).
- Raios de sol do logo como desenho recorrente (SVG que se desenha ao aparecer), ✦ ✴︎ ❋ ✺ como marcadores, fotos em arco.
- Favicon: o "A" do próprio logo, isolado em `_ref/cliente/a-logo.png`, em caramelo e sem fundo.

## Conteúdo real usado

- Bio e post fixado "Quem sou eu" (texto do Sobre).
- Destaque **Ritual** (8 stories): o que é, as 6 etapas do processo e o "Sentiu o chamado?". Os 2 depoimentos ficaram de fora por enquanto (pedido em 05/10).
- Foto da abertura: `Agatha.jpg` do zip do cliente.
- Stories de cuidados pré e pós tattoo, do endereço novo e o logo enviados pelo cliente.

## A preencher / CONFIRMAR

Campos sem dado aparecem como `<span class="a-preencher">a preencher</span>`.

1. Horários de atendimento (Início › Onde fica).
2. Fotos dos trabalhos em boa resolução: hoje são os prints de 480×640 do Instagram.
4. Classificação fine line / ornamental de cada tattoo (feita por mim, em `tools/processar.py`).
6. O ritual tem valor ou duração diferentes da sessão comum? Se sim, entra na página O Ritual.
7. Domínio.
