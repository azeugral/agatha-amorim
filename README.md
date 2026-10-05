# Agatha Amorim Tattoo Studio

Site da tatuadora Agatha Amorim ([@agathaamorim.tattoo](https://www.instagram.com/agathaamorim.tattoo/)), fine line e ornamental, em estúdio privado no Centro de Diadema - SP.
HTML, CSS e JS puros, sem build. Prévia em GitHub Pages, com `noindex` e `robots.txt` bloqueando até ter domínio.

## Painel (/admin)

O conteúdo é editado em **https://azeugral.github.io/agatha-amorim/admin/** (Sveltia CMS, interface em português).
Ao clicar em Publicar, o painel faz um commit no `main` e o GitHub Action `.github/workflows/site.yml`
converte as fotos, monta as páginas e publica no Pages, em cerca de 1 a 2 minutos.

O painel edita:
- **Trabalhos** (`conteudo/trabalhos.json`): foto, título e estilo, arrastando para ordenar. As 8 primeiras vão para a home.
- **Contato e horários**, **Início**, **O Ritual** e **Cuidados** (`conteudo/*.json`).
- As fotos enviadas vão para `conteudo/fotos/`, já convertidas em WebP de até 2048 px pelo próprio painel.

**Login:** a pessoa precisa ter uma conta no GitHub com acesso de escrita ao repositório (Settings › Collaborators).
- Hoje o login é por **"Entrar Usando Token de Acesso"**. O painel abre o link do GitHub para gerar o token, com as permissões já marcadas; é só colar o token.
- Para o botão **"Entrar com GitHub"** (um clique, recomendado para a cliente), é preciso publicar o [Sveltia CMS Authenticator](https://github.com/sveltia/sveltia-cms-auth) no Cloudflare Workers (gratuito), criar um OAuth App no GitHub apontando para ele e descomentar `base_url` em `admin/config.yml`.

## Estrutura

- `conteudo/`: **tudo o que muda**: textos em JSON e fotos originais. É o que o painel edita.
- `tools/modelos/*.html`: modelos Jinja das páginas (layout e textos fixos).
- `tools/processar.py`: fotos → `assets/obras/` (inteira e recorte 4:5), foto da abertura e `assets/js/obras.js`. Os nomes levam o hash da foto, então só converte o que mudou.
- `tools/montar_paginas.py`: modelos + conteúdo → `index.html`, `trabalhos.html`, `ritual.html`, `cuidados.html`, `agendar.html` e `404.html`. O `V` do cache de CSS/JS fica aqui.
- Os HTML da raiz, `assets/obras/` e `obras.js` são **gerados** e ficam fora do git (`.gitignore`).
- `tools/gerar_logo.py`: logo, favicon, apple-touch e `og.jpg` (roda à mão; usa `../_ref`).

Para ver localmente: `pip install -r tools/requirements.txt`, depois `python tools/processar.py` e `python tools/montar_paginas.py`.

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
