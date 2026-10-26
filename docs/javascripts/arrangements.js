/* Interactive drawings of line arrangements.
 *
 * Data: assets/data/gallery.json, written by scripts/build_gallery_data.py. Every arrangement is a list of lines
 * a x + b y + c = 0 (floats, already placed by a projective transformation chosen for legibility): "L" is the
 * certified arrangement, "S" (where present) a symmetric drawing of the same type. The intersection
 * points and the lines through each of them are computed here, with the same tolerance that the build script uses to
 * check that the drawing reproduces the certified type.
 *
 * Page hooks (all optional):
 *   <div class="lp-hero"></div>                         the pentagram with its axes, hover + idle animation
 *   <div class="lp-draw" data-n="7" data-type="5,3"></div>  one arrangement from the gallery data
 *   <div id="lp-gallery"></div>                         the full gallery with n-chips and a modal
 */
(function () {
  "use strict";
  const NS = "http://www.w3.org/2000/svg";
  const TOL = 1e-4;
  const FIELD = d => (d ? "ℚ(√" + d + ")" : "ℚ");
  const ROOT = (function () {
    const s = document.currentScript && document.currentScript.src;
    return s ? s.replace(/javascripts\/arrangements\.js.*$/, "") : "./";
  })();
  let DATA = null;
  function data() {
    if (!DATA) DATA = fetch(ROOT + "assets/data/gallery.json").then(r => r.json());
    return DATA;
  }

  /* ---------- geometry ---------- */
  function points(L) {
    const pts = [];
    for (let i = 0; i < L.length; i++) for (let j = i + 1; j < L.length; j++) {
      const [a1, b1, c1] = L[i], [a2, b2, c2] = L[j];
      const det = a1 * b2 - a2 * b1;
      if (Math.abs(det) < 1e-12) continue;
      const x = (-c1 * b2 + c2 * b1) / det, y = (-a1 * c2 + a2 * c1) / det;
      let p = pts.find(q => Math.abs(q.x - x) < TOL && Math.abs(q.y - y) < TOL);
      if (!p) { p = { x, y, lines: new Set() }; pts.push(p); }
      p.lines.add(i); p.lines.add(j);
    }
    pts.forEach(p => { p.lines = [...p.lines].sort((a, b) => a - b); p.k = p.lines.length; });
    return pts;
  }
  function clip(a, b, c, R) {
    // the chord of the line a x + b y + c = 0 inside the disc of radius R
    const n = Math.hypot(a, b); a /= n; b /= n; c /= n;
    const d = -c;
    if (Math.abs(d) >= R) return null;
    const h = Math.sqrt(R * R - d * d), px = a * d, py = b * d;
    return [px + h * b, py - h * a, px - h * b, py + h * a];
  }

  /* ---------- notation ---------- */
  // html = true: exponents as <sup> (Unicode superscript digits come from two different font blocks and do not align)
  function typeText(n, type, withTwos = true, html = true) {
    const pairs = n * (n - 1) / 2 - type.reduce((s, k) => s + k * (k - 1) / 2, 0);
    const all = withTwos ? type.concat(Array(Math.max(0, pairs)).fill(2)) : type.slice();
    if (!all.length) return "{ }";
    const parts = []; let i = 0;
    while (i < all.length) { let j = i; while (j < all.length && all[j] === all[i]) j++; parts.push(j - i > 1 ? all[i] + (html ? "<sup>" + (j - i) + "</sup>" : "^" + (j - i)) : String(all[i])); i = j; }
    return "{" + parts.join(", ") + "}";
  }
  function numText(p, d) {
    const [x, y] = p;
    if (!y) return String(x);
    const r = (y === 1 ? "" : y === -1 ? "−" : y) + "√" + d;
    if (!x) return r;
    return x + (y > 0 ? " + " : " − ") + (y < 0 ? r.replace("−", "") : r);
  }

  /* ---------- drawing ---------- */
  function el(tag, attrs, parent) {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function draw(L, opts = {}) {
    const R = opts.R || 1.2, big = !!opts.big;
    const svg = el("svg", { viewBox: `${-R} ${-R} ${2 * R} ${2 * R}`, class: "lp-svg" + (big ? " big" : ""), role: "img" });
    const g = el("g", { transform: "scale(1,-1)" }, svg);
    const lines = L.map(([a, b, c], i) => {
      const s = clip(a, b, c, R * 1.1);
      return s ? el("line", { x1: s[0], y1: s[1], x2: s[2], y2: s[3], class: "ln" }, g) : null;
    });
    const pts = points(L);
    const unit = R / 44 * (big ? 0.8 : 1);
    // colour is relative to this drawing (lightest = smallest multiplicity >= 3 present, darkest = largest),
    // size is absolute (grows with the number of lines), so pictures stay comparable by size
    const ks = [...new Set(pts.filter(p => p.k >= 3).map(p => p.k))].sort((a, b) => a - b);
    const shade = k => ks.length <= 1 ? 3 : 1 + Math.round(4 * ks.indexOf(k) / (ks.length - 1));
    pts.sort((p, q) => p.k - q.k).forEach(p => {
      const r = p.k === 2 ? unit * 0.9 : unit * (1.3 + 0.35 * (p.k - 3));
      p.el = el("circle", { cx: p.x, cy: p.y, r, class: "pt " + (p.k === 2 ? "k2" : "s" + shade(p.k)) }, g);
    });
    svg._lines = lines; svg._pts = pts; svg._ks = ks; svg._shade = shade;
    return svg;
  }
  function highlight(svg, ms) {
    const set = ms ? new Set(ms) : null;
    svg.classList.toggle("focus", !!set);
    svg._lines.forEach((ln, i) => { if (ln) ln.classList.toggle("hot", !!set && set.has(i)); });
    svg._pts.forEach(p => p.el.classList.toggle("hot", !!set && p.lines.length === set.size && p.lines.every(i => set.has(i))));
  }
  function interactive(svg, onPoint) {
    svg._pts.forEach(p => {
      if (p.k < 2) return;
      p.el.addEventListener("mouseenter", () => { highlight(svg, p.lines); if (onPoint) onPoint(p); });
      p.el.addEventListener("mouseleave", () => highlight(svg, null));
      p.el.addEventListener("click", e => { e.stopPropagation(); highlight(svg, p.lines); if (onPoint) onPoint(p); });
    });
  }

  /* ---------- hero ---------- */
  function hero(box) {
    data().then(D => {
      box.innerHTML = "";
      const svg = draw(D.star.L, { big: true, R: 1.32 });
      svg.setAttribute("aria-label", "Ten lines: a regular pentagram and its five axes of symmetry");
      box.appendChild(svg);
      interactive(svg);
      const multiple = svg._pts.filter(p => p.k >= 3);
      if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
      let i = 0, user = false, timer = null;
      const step = () => { if (user || !document.body.contains(svg)) return; highlight(svg, multiple[i % multiple.length].lines); i++; timer = setTimeout(step, 1600); };
      svg.addEventListener("mouseenter", () => { user = true; clearTimeout(timer); highlight(svg, null); });
      svg.addEventListener("mouseleave", () => { user = false; highlight(svg, null); timer = setTimeout(step, 1200); });
      timer = setTimeout(step, 900);
    });
  }

  /* ---------- single drawing ---------- */
  function single(box) {
    const n = box.dataset.n, t = (box.dataset.type || "").split(",").filter(Boolean).map(Number);
    data().then(D => {
      const it = (D.n[n] || []).find(x => x.type.join(",") === t.join(","));
      if (!it) return;
      box.innerHTML = "";
      const svg = draw(it.L); box.appendChild(svg); interactive(svg);
    });
  }

  /* ---------- gallery ---------- */
  const MODES = { beautiful: "Beautiful", exact: "Exact" };
  const pick = (it, mode) => (mode === "beautiful" && it.S ? it.S : it.L);
  function symText(it) { return it.rot >= 3 ? "a symmetry group of order " + it.sym : "a mirror symmetry"; }
  function gallery(root) {
    data().then(D => {
      const ns = Object.keys(D.n).map(Number).sort((a, b) => a - b);
      let cur = 10, mode = "beautiful";
      try { const v = +localStorage.getItem("lp-n"); if (D.n[v]) cur = v; } catch (e) {}
      try { const m = localStorage.getItem("lp-mode"); if (MODES[m]) mode = m; } catch (e) {}
      root.innerHTML = `<div class="lp-modes" role="tablist" aria-label="Drawing style"></div><p class="lp-modenote"></p>` +
        `<div class="lp-chips lp-ns" role="tablist" aria-label="Number of lines"></div><p class="lp-summary"></p><div class="lp-grid"></div>`;
      const chips = root.querySelector(".lp-ns"), grid = root.querySelector(".lp-grid"), summ = root.querySelector(".lp-summary");
      const modes = root.querySelector(".lp-modes"), note = root.querySelector(".lp-modenote");
      Object.keys(MODES).forEach(m => {
        const b = document.createElement("button");
        b.type = "button"; b.className = "lp-chip lp-mode"; b.dataset.mode = m; b.textContent = MODES[m]; b.setAttribute("role", "tab");
        b.addEventListener("click", () => { mode = m; try { localStorage.setItem("lp-mode", m); } catch (e) {} show(cur); });
        modes.appendChild(b);
      });
      ns.forEach(n => {
        const b = document.createElement("button");
        b.type = "button"; b.className = "lp-chip"; b.textContent = n; b.setAttribute("role", "tab");
        b.addEventListener("click", () => show(n));
        chips.appendChild(b);
      });
      const io = "IntersectionObserver" in window ? new IntersectionObserver(es => es.forEach(e => {
        if (!e.isIntersecting) return;
        const card = e.target; io.unobserve(card);
        card.querySelector(".lp-art").appendChild(draw(pick(card._it, mode)));
      }), { rootMargin: "300px" }) : null;
      function show(n) {
        cur = n;
        try { localStorage.setItem("lp-n", n); } catch (e) {}
        chips.querySelectorAll(".lp-chip").forEach(c => c.setAttribute("aria-selected", +c.textContent === n ? "true" : "false"));
        modes.querySelectorAll(".lp-mode").forEach(c => c.setAttribute("aria-selected", c.dataset.mode === mode ? "true" : "false"));
        note.textContent = mode === "beautiful"
          ? "Symmetric drawings, built from regular polygons, the symmetry axes of polyhedra and sections of 4-dimensional mirror arrangements. Types without one are drawn as under Exact."
          : "The certified arrangements, drawn from their exact coordinates.";
        const items = D.n[n];
        const f0s = [...new Set(items.map(it => it.f0))].sort((a, b) => a - b);
        const nsym = items.filter(it => it.S).length;
        summ.textContent = n <= 2
          ? (n === 1 ? "One line: no intersection point." : "Two lines: one intersection point.")
          : `${items.length} pencil types drawn for ${n} lines; numbers of intersection points: ${f0s.join(", ")}.` +
            (mode === "beautiful" ? ` ${nsym} of them have a symmetric drawing.` : "") +
            (n >= 13 ? " For this n the list is a lower bound." : "");
        grid.innerHTML = "";
        items.forEach(it => {
          const card = document.createElement("button");
          card.type = "button"; card.className = "lp-card";
          const sym = mode === "beautiful" && it.S ? " · " + (it.rot >= 3 ? "order " + it.sym : "mirror") : "";
          card.innerHTML = `<div class="lp-art"></div><div class="lp-cap"><span class="lp-type">${typeText(n, it.type)}</span><span class="lp-meta">f₀ = ${it.f0}${it.d ? " · " + FIELD(it.d) : ""}${sym}</span></div>`;
          card.setAttribute("aria-label", `Type ${typeText(n, it.type, true, false)}, ${it.f0} intersection points`);
          card._it = it;
          card.addEventListener("click", () => modal(n, it, mode));
          grid.appendChild(card);
          if (io) io.observe(card); else card.querySelector(".lp-art").appendChild(draw(pick(it, mode)));
        });
      }
      show(cur);
    });
  }

  function sourceText(src) {
    if (!src) return "";
    if (/^legacy search/.test(src)) return "Found by a search over integer and algebraic point sets.";
    if (/^band construction/.test(src)) return "Built from a smaller arrangement by adding a pencil through chosen points (band theorem).";
    if (/rich line/.test(src) || /^extension/.test(src)) return "Built by adding a line through existing intersection points.";
    if (/numerical realization/.test(src)) return "Found by solving the incidence equations numerically and recovering exact coordinates.";
    return "";
  }

  /* ---------- modal ---------- */
  function modal(n, it, mode) {
    if (!it.S) mode = "exact";
    const m = document.createElement("div");
    m.className = "lp-modal"; m.setAttribute("role", "dialog"); m.setAttribute("aria-modal", "true");
    const pencils = it.type.length ? it.type.length + (it.type.length === 1 ? " point" : " points") + " on three or more lines" : "no point on three or more lines";
    const t2 = n * (n - 1) / 2 - it.type.reduce((s, k) => s + k * (k - 1) / 2, 0);
    m.innerHTML = `<div class="lp-dialog">
      <button type="button" class="lp-close" aria-label="Close">×</button>
      <div class="lp-big"></div>
      <div class="lp-info">
        <div class="lp-eyebrow">${n} lines</div>
        <h2>${typeText(n, it.type)}</h2>
        <div class="lp-chips lp-tabs" role="tablist" aria-label="Drawing style"></div>
        <p class="lp-view"></p>
        <p>${it.f0} intersection points: ${pencils}${t2 ? " and " + t2 + " ordinary crossing" + (t2 === 1 ? "" : "s") : ""}.
        Coordinates of the certificate lie in ${FIELD(it.d)}.</p>
        <p class="lp-keys"></p>
        <p class="lp-hint">Point at an intersection to see the lines through it.</p>
        <div class="lp-now"></div>
        <details class="lp-exact"><summary>Exact lines <i>a x + b y + c z = 0</i></summary><ol class="lp-coef"></ol></details>
        <p class="lp-src">${sourceText(it.source)}</p>
      </div></div>`;
    document.body.appendChild(m);
    document.documentElement.classList.add("lp-noscroll");
    const now = m.querySelector(".lp-now"), big = m.querySelector(".lp-big"), view = m.querySelector(".lp-view");
    const tabs = m.querySelector(".lp-tabs"), exact = m.querySelector(".lp-exact");
    let svg = null;
    function render(md) {
      mode = md;
      tabs.querySelectorAll(".lp-chip").forEach(c => c.setAttribute("aria-selected", c.dataset.mode === md ? "true" : "false"));
      big.innerHTML = ""; now.textContent = "";
      svg = draw(pick(it, md), { big: true });
      big.appendChild(svg);
      m.querySelector(".lp-keys").innerHTML = svg._ks.map(k => `<span><i class="s${svg._shade(k)}"></i>${k} lines</span>`).join("") +
        `<span><i class="k2"></i>2 lines</span>`;
      interactive(svg, p => { now.textContent = p.k + " lines meet here" + (md === "exact" ? ": " + p.lines.map(i => "ℓ" + (i + 1)).join(", ") : "") + "."; });
      view.textContent = md === "beautiful"
        ? `${it.how} The drawing has ${symText(it)}. It is a floating-point realization of the same type, checked with the same tolerance as the exact drawing; the certificate is shown under Exact, and the two arrangements need not be projective images of each other.`
        : "The certified arrangement, drawn from its exact coordinates by a projective transformation chosen for legibility.";
      exact.hidden = md !== "exact";
      m.querySelector(".lp-src").hidden = md !== "exact";
    }
    if (it.S) {
      Object.keys(MODES).forEach(md => {
        const b = document.createElement("button");
        b.type = "button"; b.className = "lp-chip"; b.dataset.mode = md; b.textContent = MODES[md]; b.setAttribute("role", "tab");
        b.addEventListener("click", () => render(md));
        tabs.appendChild(b);
      });
    } else tabs.hidden = true;
    const ol = m.querySelector(".lp-coef");
    it.exact.forEach((line, i) => {
      const li = document.createElement("li");
      li.textContent = "ℓ" + (i + 1) + ": (" + line.map(p => numText(p, it.d)).join(", ") + ")";
      li.addEventListener("mouseenter", () => { if (mode === "exact") highlight(svg, [i]); });
      li.addEventListener("mouseleave", () => highlight(svg, null));
      ol.appendChild(li);
    });
    render(mode);
    function close() { m.remove(); document.documentElement.classList.remove("lp-noscroll"); document.removeEventListener("keydown", key); }
    function key(e) { if (e.key === "Escape") close(); }
    m.addEventListener("click", e => { if (e.target === m) close(); });
    m.querySelector(".lp-close").addEventListener("click", close);
    document.addEventListener("keydown", key);
    m.querySelector(".lp-close").focus();
  }

  /* ---------- boot ---------- */
  function boot() {
    document.querySelectorAll(".lp-hero").forEach(hero);
    document.querySelectorAll(".lp-draw").forEach(single);
    const g = document.getElementById("lp-gallery");
    if (g) gallery(g);
  }
  if (window.document$) window.document$.subscribe(boot);
  else document.addEventListener("DOMContentLoaded", boot);
})();
