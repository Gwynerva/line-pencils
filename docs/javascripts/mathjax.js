window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex",
    enableMenu: false            // the context menu is not needed on this site
  }
};

/* Keep punctuation that directly follows an inline formula on the same line as the formula:
   "…$f_0$." must not break before the full stop. The formula and the punctuation are wrapped
   together in a span that does not wrap. Runs before typesetting, on the arithmatex source spans. */
function gluePunctuation(root) {
  root.querySelectorAll("span.arithmatex").forEach(el => {
    if (el.parentNode && el.parentNode.classList && el.parentNode.classList.contains("nobr")) return;
    const next = el.nextSibling;
    if (!next || next.nodeType !== Node.TEXT_NODE) return;
    const m = next.nodeValue.match(/^[.,;:!?)\]’”]+/);
    if (!m) return;
    const wrap = document.createElement("span");
    wrap.className = "nobr";
    el.parentNode.insertBefore(wrap, el);
    wrap.appendChild(el);
    wrap.appendChild(document.createTextNode(m[0]));
    next.nodeValue = next.nodeValue.slice(m[0].length);
  });
}

document$.subscribe(() => {
  gluePunctuation(document);
  if (!window.MathJax || !MathJax.startup || !MathJax.startup.output) return;
  MathJax.startup.output.clearCache();
  MathJax.typesetClear();
  MathJax.texReset();
  MathJax.typesetPromise();
});
