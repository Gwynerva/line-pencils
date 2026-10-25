"""Checks on the built site (site/): no TeX left unrendered by the Markdown stage and no broken internal links.

A '$' in visible text outside code and outside the spans that arithmatex hands to MathJax means that a formula was
not recognised (typically TeX inside raw HTML, or '$ ' before a closing dollar).

usage: python scripts/check_site.py        exit status 1 if a problem is found
"""
import glob, html, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
bad = 0
for f in sorted(glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True)):
    s = open(f, encoding="utf-8").read()
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
    body = re.sub(r'<(span|div) class="arithmatex">.*?</\1>', "", body, flags=re.S)
    body = re.sub(r"<pre.*?</pre>|<code.*?</code>", "", body, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    for m in re.finditer(r"\$", text):
        bad += 1
        print("raw $ in %s: ...%s..." % (os.path.relpath(f, SITE), text[max(0, m.start() - 40):m.start() + 40].replace("\n", " ")))
    for href in re.findall(r'href="([^"#:?]+)(?:#[^"]*)?"', s):
        if href.startswith(("http", "mailto", "//")) or href.endswith((".css", ".js", ".svg", ".png", ".ico", ".xml", ".json")):
            continue
        if href.startswith("/line-pencils/"):
            target = os.path.normpath(os.path.join(SITE, href[len("/line-pencils/"):]))
        else:
            target = os.path.normpath(os.path.join(os.path.dirname(f), href))
        if os.path.isdir(target):
            target = os.path.join(target, "index.html")
        if not os.path.exists(target):
            bad += 1
            print("broken link in %s: %s" % (os.path.relpath(f, SITE), href))
print("site check:", "OK" if not bad else "%d problems" % bad)
sys.exit(1 if bad else 0)
