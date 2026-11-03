/* Rotating drawings of plane arrangements (docs/planes.md).
 *
 * Data: assets/data/planes3d.json, written by scripts/build_planes3d.py: for each scene the planes (unit normal n,
 * offset d: n.x = d), the points and lines with the planes through them, all finite and inside the ball of radius R
 * to which the planes are clipped.
 *
 * Page hook: <div class="lp-planes" data-scene="book"></div>
 *
 * The planes are translucent discs. They are drawn back to front in the order of a BSP tree whose splitting planes
 * are the planes themselves, so the order is exact from every direction. Lines are drawn on top, fainter at the
 * back, and the points on top of everything. The drawing turns slowly, can be turned by dragging, and hovering a
 * point shows the planes through it.
 */
(function () {
  "use strict";
  const ROOT = (function () {
    const s = document.currentScript && document.currentScript.src;
    return s ? s.replace(/javascripts\/planes3d\.js.*$/, "") : "./";
  })();
  let DATA = null;
  const data = () => DATA || (DATA = fetch(ROOT + "assets/data/planes3d.json").then(r => r.json()));
  const reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  const add = (a, b, t) => [a[0] + t * b[0], a[1] + t * b[1], a[2] + t * b[2]];
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const unit = a => { const k = Math.hypot(a[0], a[1], a[2]); return [a[0] / k, a[1] / k, a[2] / k]; };

  /* ---------- geometry: discs, BSP tree ---------- */
  function disc(plane, i, R, m = 96) {
    const n = plane.slice(0, 3), d = plane[3];
    const c = [n[0] * d, n[1] * d, n[2] * d], r = Math.sqrt(Math.max(0, R * R - d * d));
    const u = unit(cross(n, Math.abs(n[0]) < 0.9 ? [1, 0, 0] : [0, 1, 0])), v = cross(n, u);
    const vs = [];
    for (let k = 0; k < m; k++) {
      const t = 2 * Math.PI * k / m;
      vs.push(add(add(c, u, r * Math.cos(t)), v, r * Math.sin(t)));
    }
    return { plane: i, vs, rim: vs.map(() => true) };
  }
  function split(poly, n, d) {
    // pieces of poly on the front (n.x > d) and back side; rim[k] marks the edge vs[k] -> vs[k+1] as part of the disc rim
    const F = { plane: poly.plane, vs: [], rim: [] }, B = { plane: poly.plane, vs: [], rim: [] };
    const s = poly.vs.map(x => dot(n, x) - d), m = poly.vs.length;
    for (let k = 0; k < m; k++) {
      const a = poly.vs[k], b = poly.vs[(k + 1) % m], sa = s[k], sb = s[(k + 1) % m], r = poly.rim[k];
      if (sa >= 0) { F.vs.push(a); F.rim.push(r); }
      if (sa <= 0) { B.vs.push(a); B.rim.push(r); }
      if ((sa > 0 && sb < 0) || (sa < 0 && sb > 0)) {
        const t = sa / (sa - sb), p = [a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]), a[2] + t * (b[2] - a[2])];
        // the edge leaving the crossing point continues the rim on one side and runs along the cut on the other
        if (sa > 0) { F.vs.push(p); F.rim.push(false); B.vs.push(p); B.rim.push(r); }
        else { B.vs.push(p); B.rim.push(false); F.vs.push(p); F.rim.push(r); }
      }
    }
    return [F.vs.length >= 3 ? F : null, B.vs.length >= 3 ? B : null];
  }
  function bsp(polys, planes) {
    if (!polys.length) return null;
    const [root, ...rest] = polys, P = planes[root.plane], n = P.slice(0, 3), d = P[3];
    const front = [], back = [];
    rest.forEach(p => { const [f, b] = split(p, n, d); if (f) front.push(f); if (b) back.push(b); });
    return { n, d, poly: root, front: bsp(front, planes), back: bsp(back, planes) };
  }
  function walk(node, view, out) {
    if (!node) return;
    const near = dot(node.n, view) > 0;
    walk(near ? node.back : node.front, view, out);
    out.push(node.poly);
    walk(near ? node.front : node.back, view, out);
  }

  /* ---------- colours ---------- */
  function palette(el) {
    const cs = getComputedStyle(el), dark = document.body.getAttribute("data-md-color-scheme") === "slate";
    const v = k => cs.getPropertyValue(k).trim();
    return { dark, hot: dark ? v("--lp-s4") : v("--lp-hot"), line: v("--lp-line"), pt: v("--lp-s3"), pt3: v("--lp-k2"), bg: v("--md-default-bg-color") };
  }
  const hue = (i, n) => (205 + 360 * i / n) % 360;

  /* ---------- one drawing ---------- */
  function draw(el, S) {
    const R = S.R, planes = S.planes;
    const tree = bsp(planes.map((p, i) => disc(p, i, R)), planes);
    const segs = S.lines.map(L => {
      const b = dot(L.at, L.dir), c = dot(L.at, L.at) - R * R, h = Math.sqrt(Math.max(0, b * b - c));
      return { a: add(L.at, L.dir, -b - h), b: add(L.at, L.dir, -b + h), k: L.on.length, on: L.on };
    });
    const pts = S.points.map(P => ({ x: P.at, k: P.on.length, on: P.on }));

    const canvas = document.createElement("canvas");
    el.append(canvas);
    const ctx = canvas.getContext("2d");
    let yaw = 0.6, pitch = 0.35, drag = null, hover = null, visible = true, last = 0, col = palette(el);

    function rot() {
      const cy = Math.cos(yaw), sy = Math.sin(yaw), cp = Math.cos(pitch), sp = Math.sin(pitch);
      // rows of Rx(pitch) * Ry(yaw)
      return [[cy, 0, sy], [sp * sy, cp, -sp * cy], [-cp * sy, sp, cp * cy]];
    }
    function render() {
      const dpr = window.devicePixelRatio || 1, W = el.clientWidth;
      if (canvas.width !== Math.round(W * dpr)) { canvas.width = Math.round(W * dpr); canvas.height = canvas.width; }
      const w = canvas.width, s = w / 2 / (R * 1.04), M = rot(), view = M[2], z = dpr * Math.min(1.5, Math.max(1, W / 340));
      const P = x => [w / 2 + s * dot(M[0], x), w / 2 - s * dot(M[1], x), dot(M[2], x)];
      ctx.clearRect(0, 0, w, w);
      const order = [];
      walk(tree, view, order);
      const n = planes.length, L = col.dark ? 62 : 52;
      for (const poly of order) {
        const on = !hover || hover.on.includes(poly.plane);
        const face = Math.abs(dot(planes[poly.plane], view));
        const h = hue(poly.plane, n);
        ctx.beginPath();
        poly.vs.forEach((x, k) => { const q = P(x); k ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); });
        ctx.closePath();
        ctx.fillStyle = `hsla(${h},58%,${L}%,${on ? (hover ? 0.42 : 0.14 + 0.16 * face) : 0.04})`;
        ctx.fill();
        ctx.lineWidth = 1.2 * z;
        ctx.strokeStyle = `hsla(${h},58%,${L - 8}%,${on ? 0.75 : 0.15})`;
        ctx.beginPath();
        poly.vs.forEach((x, k) => {
          if (!poly.rim[k]) return;
          const a = P(x), b = P(poly.vs[(k + 1) % poly.vs.length]);
          ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]);
        });
        ctx.stroke();
      }
      // lines and points, back to front, fainter at the back
      const items = [];
      segs.forEach(g => { const a = P(g.a), b = P(g.b); items.push({ z: (a[2] + b[2]) / 2, g, a, b }); });
      pts.forEach(p => { const q = P(p.x); items.push({ z: q[2], p, q }); });
      // lines back to front, then all points on top of everything
      items.sort((u, v) => (u.p ? 1 : 0) - (v.p ? 1 : 0) || u.z - v.z);
      for (const it of items) {
        const fade = 0.55 + 0.45 * (it.z / R + 1) / 2;
        if (it.g) {
          const sp = it.g.k >= 3, lit = hover && it.g.on.every(i => hover.on.includes(i));
          ctx.globalAlpha = (hover && !lit ? 0.25 : 1) * fade * (sp ? 1 : 0.7);
          ctx.lineCap = "round";
          if (sp) {  // a halo in the background colour keeps the line readable over the coloured planes
            ctx.strokeStyle = col.bg;
            ctx.lineWidth = 6.4 * z;
            ctx.beginPath(); ctx.moveTo(it.a[0], it.a[1]); ctx.lineTo(it.b[0], it.b[1]); ctx.stroke();
          }
          ctx.strokeStyle = sp ? col.hot : col.line;
          ctx.lineWidth = (sp ? 3.2 : 1.1) * z;
          ctx.beginPath(); ctx.moveTo(it.a[0], it.a[1]); ctx.lineTo(it.b[0], it.b[1]); ctx.stroke();
        } else {
          const p = it.p, big = p.k >= 4, r = (big ? 4.4 + 1.4 * (p.k - 4) : 3) * z * (p === hover ? 1.5 : 1);
          ctx.globalAlpha = (hover && p !== hover ? 0.35 : 1) * fade;
          ctx.fillStyle = big ? col.pt : col.pt3;
          ctx.strokeStyle = col.bg;
          ctx.lineWidth = 1.2 * z;
          ctx.beginPath(); ctx.arc(it.q[0], it.q[1], r, 0, 2 * Math.PI); ctx.fill(); ctx.stroke();
        }
      }
      ctx.globalAlpha = 1;
      return P;
    }
    let proj = render();

    function frame(t) {
      if (!visible) { last = 0; return; }
      if (last && !drag && !hover && !reduced) yaw += Math.min(50, t - last) * 0.00025;
      last = t;
      proj = render();
      requestAnimationFrame(frame);
    }
    new IntersectionObserver(es => {
      const was = visible;
      visible = es[0].isIntersecting;
      if (visible && !was) requestAnimationFrame(frame);
    }).observe(el);
    requestAnimationFrame(frame);
    new MutationObserver(() => { col = palette(el); }).observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });

    canvas.addEventListener("pointerdown", e => { drag = [e.clientX, e.clientY, yaw, pitch]; canvas.setPointerCapture(e.pointerId); });
    canvas.addEventListener("pointerup", () => { drag = null; });
    canvas.addEventListener("pointercancel", () => { drag = null; });
    canvas.addEventListener("pointerleave", () => { if (!drag) hover = null; });
    canvas.addEventListener("pointermove", e => {
      if (drag) {
        yaw = drag[2] + (e.clientX - drag[0]) * 0.01;
        pitch = Math.max(-1.4, Math.min(1.4, drag[3] + (e.clientY - drag[1]) * 0.01));
        return;
      }
      const r = canvas.getBoundingClientRect(), k = canvas.width / r.width;
      const x = (e.clientX - r.left) * k, y = (e.clientY - r.top) * k;
      let best = null, bd = 14 * k;
      pts.forEach(p => { const q = proj(p.x), dd = Math.hypot(q[0] - x, q[1] - y); if (dd < bd) { bd = dd; best = p; } });
      hover = best;
    });
  }

  function boot() {
    const els = document.querySelectorAll(".lp-planes:not([data-done])");
    if (!els.length) return;
    data().then(D => els.forEach(el => { el.dataset.done = "1"; if (D[el.dataset.scene]) draw(el, D[el.dataset.scene]); }));
  }
  if (window.document$) window.document$.subscribe(boot);
  else document.addEventListener("DOMContentLoaded", boot);
})();
