// Agatha Amorim Tattoo Studio — comportamento comum às páginas
// o número vem de conteudo/contato.json (editável no painel), gravado no <body data-whatsapp>
const CONFIG = {
  whatsapp: (document.body.dataset.whatsapp || "").replace(/\D/g, ""),
};

const ESTILOS = { fineline: "Fine line", ornamental: "Ornamental", escrita: "Escrita" };
const reduzido = matchMedia("(prefers-reduced-motion: reduce)").matches;

/* ---------- contato ---------- */
function enviarMensagem(texto) {
  location.href = `https://wa.me/${CONFIG.whatsapp}?text=${encodeURIComponent(texto)}`;
}
document.addEventListener("click", (e) => {
  const a = e.target.closest("[data-contato]");
  if (!a) return;
  e.preventDefault();
  enviarMensagem(a.dataset.contato || "Oi, Agatha! Quero fazer uma tattoo.");
});

/* ---------- topo e menu ---------- */
const topo = document.querySelector(".topo");
const btnMenu = document.querySelector(".menu-btn");
const nav = document.querySelector(".nav");
function menu(abrir) {
  btnMenu.setAttribute("aria-expanded", String(abrir));
  btnMenu.setAttribute("aria-label", abrir ? "Fechar menu" : "Abrir menu");
  nav.classList.toggle("aberto", abrir);
  document.body.classList.toggle("menu-aberto", abrir);
}
if (btnMenu) {
  btnMenu.addEventListener("click", () => menu(btnMenu.getAttribute("aria-expanded") !== "true"));
  addEventListener("keydown", (e) => { if (e.key === "Escape" && nav.classList.contains("aberto")) menu(false); });
  matchMedia("(min-width: 821px)").addEventListener("change", () => menu(false));
}
const marcarTopo = () => topo.classList.toggle("rolou", scrollY > 8);
addEventListener("scroll", marcarTopo, { passive: true });
marcarTopo();

/* ---------- raios de sol (o mesmo gesto do logo) ---------- */
function montarRaios(svg) {
  const g = svg.querySelector("g");
  const n = 15, cx = 100, cy = 100;
  let html = "";
  for (let i = 0; i < n; i++) {
    const ang = Math.PI + (Math.PI * i) / (n - 1);          // meia-volta, de 180° a 360°
    const r1 = 30, r2 = i % 2 ? 72 : 92;
    const x1 = cx + Math.cos(ang) * r1, y1 = cy + Math.sin(ang) * r1;
    const x2 = cx + Math.cos(ang) * r2, y2 = cy + Math.sin(ang) * r2;
    html += `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" pathLength="1" style="transition-delay:${(i * 0.045).toFixed(3)}s"/>`;
  }
  g.innerHTML = html;
}
document.querySelectorAll("svg.raios").forEach(montarRaios);

/* ---------- revelar ao rolar (só abaixo da dobra) ---------- */
function revelar() {
  const els = document.querySelectorAll(".revela, svg.raios");
  const acender = (el) => el.classList.add(el.matches("svg") ? "acesos" : "visivel");
  if (reduzido || !("IntersectionObserver" in window)) { els.forEach(acender); return; }
  const io = new IntersectionObserver((ents) => {
    ents.forEach((en) => { if (en.isIntersecting) { acender(en.target); io.unobserve(en.target); } });
  }, { rootMargin: "0px 0px -8% 0px" });
  els.forEach((el) => {
    if (el.getBoundingClientRect().top < innerHeight) requestAnimationFrame(() => requestAnimationFrame(() => acender(el)));
    else io.observe(el);
  });
}
if (!reduzido) document.querySelectorAll(".abertura__txt > *").forEach((el) => el.classList.add("entra"));

/* ---------- grade de trabalhos ---------- */
function cartao(o, i) {
  const est = ESTILOS[o.estilo];
  return `<figure class="obra" role="button" tabindex="0" data-i="${i}" aria-label="${o.titulo}, ${est}. Ampliar">
    <img src="assets/obras/${o.slug}-t.webp?v=2" alt="Tattoo ${o.titulo}, ${est}" width="800" height="1000" loading="lazy" decoding="async">
    <figcaption>${o.titulo} · ${est}</figcaption>
  </figure>`;
}

function montarGrade(grade) {
  const todas = window.OBRAS || [];
  const limite = Number(grade.dataset.limite) || 0;
  const filtros = document.querySelector(".filtros");
  let lista = todas;

  const desenhar = () => {
    const estilo = filtros ? location.hash.slice(1) : "";
    lista = ESTILOS[estilo] ? todas.filter((o) => o.estilo === estilo) : todas;
    if (limite) lista = lista.slice(0, limite);
    grade.innerHTML = lista.map(cartao).join("");
    if (filtros) filtros.querySelectorAll("a").forEach((a) => a.setAttribute("aria-current", String(a.hash.slice(1) === (ESTILOS[estilo] ? estilo : "todos"))));
  };
  desenhar();

  if (filtros) {
    filtros.addEventListener("click", (e) => {
      const a = e.target.closest("a");
      if (!a) return;
      e.preventDefault();
      if (a.hash === location.hash || (!location.hash && a.hash === "#todos")) return;
      history.replaceState(null, "", a.hash);
      trocar();
    });
    addEventListener("hashchange", trocar);
  }
  function trocar() {
    if (reduzido) return desenhar();
    grade.classList.add("trocando");
    setTimeout(() => { desenhar(); requestAnimationFrame(() => requestAnimationFrame(() => grade.classList.remove("trocando"))); }, 220);
  }

  const abrir = (el) => ampliar(lista, Number(el.dataset.i));
  grade.addEventListener("click", (e) => { const el = e.target.closest(".obra"); if (el) abrir(el); });
  grade.addEventListener("keydown", (e) => {
    const el = e.target.closest(".obra");
    if (el && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); abrir(el); }
  });
}

/* ---------- visualização ampliada ---------- */
let amplia, voltarFoco;
function ampliar(lista, i) {
  if (!amplia) {
    amplia = document.createElement("div");
    amplia.className = "amplia";
    amplia.setAttribute("role", "dialog");
    amplia.setAttribute("aria-modal", "true");
    amplia.setAttribute("aria-label", "Trabalho ampliado");
    amplia.innerHTML = `
      <img alt="">
      <p class="amplia__legenda"></p>
      <button class="amplia__fechar" aria-label="Fechar"><svg viewBox="0 0 32 32"><path d="M8 8l16 16M24 8L8 24"/></svg></button>
      <button class="amplia__ant" aria-label="Anterior"><svg viewBox="0 0 32 32"><path d="M20 6L10 16l10 10"/></svg></button>
      <button class="amplia__prox" aria-label="Próxima"><svg viewBox="0 0 32 32"><path d="M12 6l10 10-10 10"/></svg></button>`;
    document.body.append(amplia);
  }
  voltarFoco = document.activeElement;
  const img = amplia.querySelector("img");
  const leg = amplia.querySelector(".amplia__legenda");
  let atual = i;
  const mostrar = (n) => {
    atual = (n + lista.length) % lista.length;
    const o = lista[atual];
    img.style.opacity = 0;
    const nova = new Image();
    nova.onload = () => { img.src = nova.src; img.alt = `Tattoo ${o.titulo}`; img.style.opacity = 1; };
    nova.src = `assets/obras/${o.slug}.webp?v=2`;
    leg.textContent = `${o.titulo} · ${ESTILOS[o.estilo]} · ${atual + 1}/${lista.length}`;
  };
  const fechar = () => {
    amplia.classList.remove("aberta");
    document.body.style.overflow = "";
    removeEventListener("keydown", teclas);
    if (voltarFoco) voltarFoco.focus({ preventScroll: true });
  };
  const teclas = (e) => {
    if (e.key === "Escape") fechar();
    if (e.key === "ArrowLeft") mostrar(atual - 1);
    if (e.key === "ArrowRight") mostrar(atual + 1);
  };
  amplia.onclick = (e) => {
    if (e.target.closest(".amplia__ant")) return mostrar(atual - 1);
    if (e.target.closest(".amplia__prox")) return mostrar(atual + 1);
    if (e.target === amplia || e.target.closest(".amplia__fechar")) fechar();
  };
  // arrastar para trocar no toque
  let x0 = null;
  img.onpointerdown = (e) => { x0 = e.clientX; };
  img.onpointercancel = () => { x0 = null; };
  img.onpointerup = (e) => {
    if (x0 === null) return;
    const dx = e.clientX - x0; x0 = null;
    if (Math.abs(dx) > 50) mostrar(atual + (dx < 0 ? 1 : -1));
  };
  addEventListener("keydown", teclas);
  document.body.style.overflow = "hidden";
  mostrar(i);
  requestAnimationFrame(() => amplia.classList.add("aberta"));
  amplia.querySelector(".amplia__fechar").focus({ preventScroll: true });
}

/* ---------- agendar ---------- */
function montarOrcamento(form) {
  const aviso = form.querySelector(".aviso");
  if (new URLSearchParams(location.search).has("ritual")) form.querySelector('[name="ritual"]').checked = true;
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const d = new FormData(form);
    const v = (k) => (d.get(k) || "").toString().trim();
    if (!v("nome") || !v("ideia")) {
      aviso.textContent = "Preencha pelo menos o nome e a ideia.";
      form.querySelector(v("nome") ? '[name="ideia"]' : '[name="nome"]').focus();
      return;
    }
    const se = (cond, txt) => (cond ? txt : null);
    const linhas = [
      `Oi, Agatha! Meu nome é ${v("nome")} e quero fazer uma tattoo.`,
      "",
      `Ideia / intenção: ${v("ideia")}`,
      se(v("arte"), `Arte: ${v("arte")}`),
      se(v("ritual"), "Quero viver o ritual de tattoo."),
      se(v("estilo"), `Estilo: ${v("estilo")}`),
      se(v("local"), `Local do corpo: ${v("local")}`),
      se(v("tamanho"), `Tamanho aproximado: ${v("tamanho")}`),
      se(v("primeira"), `Primeira tattoo: ${v("primeira")}`),
      se(v("dias"), `Melhores dias: ${v("dias")}`),
      "",
      "Vou mandar as referências por aqui.",
    ].filter((l) => l !== null);
    aviso.textContent = "Abrindo o WhatsApp…";
    enviarMensagem(linhas.join("\n"));
  });
}

/* ---------- início ---------- */
document.querySelectorAll("[data-grade]").forEach(montarGrade);
document.querySelectorAll("form[data-orcamento]").forEach(montarOrcamento);
revelar();
const ano = document.querySelector("[data-ano]");
if (ano) ano.textContent = new Date().getFullYear();
