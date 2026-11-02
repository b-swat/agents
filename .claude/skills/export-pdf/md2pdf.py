#!/usr/bin/env python3
"""Export a Markdown document (with Mermaid diagrams) to PDF next to it.

Usage: md2pdf.py <file.md> [<file.md> ...]

Tools: python3 + markdown-it-py (HTML), local mermaid.min.js (diagrams), headless Chrome/Chromium/Edge (PDF).
Works offline on macOS and Ubuntu. Browser override: MD2PDF_BROWSER=/path/to/browser.
The .md stays the source of truth; the .pdf is an export copy.
"""
import html
import os
import shutil
import re
import subprocess
import sys
from pathlib import Path

from markdown_it import MarkdownIt

SKILL_DIR = Path(__file__).resolve().parent
MERMAID_JS = SKILL_DIR / "vendor" / "mermaid.min.js"
BROWSER_NAMES = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge"]
MACOS_BROWSERS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]

CSS = """
@page { size: A4; margin: 18mm 15mm; }
body { font-family: "DejaVu Sans", Arial, sans-serif; font-size: 10.5pt; line-height: 1.45; color: #111; }
h1 { font-size: 18pt; border-bottom: 2px solid #333; padding-bottom: 4px; }
h2 { font-size: 14pt; border-bottom: 1px solid #aaa; padding-bottom: 2px; margin-top: 1.4em; }
h3 { font-size: 12pt; }
table { border-collapse: collapse; width: 100%; margin: 0.6em 0; page-break-inside: auto; }
th, td { border: 1px solid #999; padding: 4px 6px; vertical-align: top; text-align: left; }
th { background: #eee; }
tr { page-break-inside: avoid; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 9.5pt; background: #f3f3f3; padding: 0 2px; }
pre { background: #f6f6f6; border: 1px solid #ddd; padding: 6px; white-space: pre-wrap; page-break-inside: avoid; }
pre code { background: none; padding: 0; }
.mermaid { text-align: center; page-break-inside: avoid; margin: 0.8em 0; background: none; border: none; }
.mermaid svg { max-width: 100% !important; max-height: 235mm; width: auto !important; height: auto; }
"""


def find_browser() -> str:
    override = os.environ.get("MD2PDF_BROWSER")
    if override:
        return override
    for name in BROWSER_NAMES:
        path = shutil.which(name)
        if path:
            return path
    for path in MACOS_BROWSERS + [str(Path.home()) + p for p in MACOS_BROWSERS]:
        if Path(path).exists():
            return path
    raise RuntimeError("No Chrome/Chromium/Edge found; install one or set MD2PDF_BROWSER")


def render_html(md_path: Path) -> str:
    text = re.sub(r"<!--.*?-->", "", md_path.read_text(encoding="utf-8"), flags=re.DOTALL)
    md = MarkdownIt("commonmark", {"html": False}).enable("table").enable("strikethrough")
    default_fence = md.renderer.rules.get("fence")

    def fence(renderer, tokens, idx, options, env):
        token = tokens[idx]
        if token.info.strip().lower() == "mermaid":
            return f'<pre class="mermaid">{html.escape(token.content)}</pre>\n'
        return default_fence(tokens, idx, options, env)

    md.add_render_rule("fence", fence)
    body = md.render(text)

    version = re.search(r"^\|\s*Version\s*\|\s*([^|]+?)\s*\|", text, re.MULTILINE)
    title = md_path.stem + (f" — v{version.group(1)}" if version else "")
    mermaid_js = MERMAID_JS.read_text(encoding="utf-8")
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>{CSS}</style>
<script>{mermaid_js}</script>
<script>mermaid.initialize({{ startOnLoad: true, theme: "neutral", securityLevel: "loose" }});</script>
</head><body>
{body}
</body></html>"""


def export(md_path: Path) -> Path:
    pdf_path = md_path.with_suffix(".pdf")
    # The temporary HTML sits next to the .md so the PDF footer shows the document's own location.
    html_path = md_path.with_name(f".{md_path.stem}.export.html")
    html_path.write_text(render_html(md_path), encoding="utf-8")
    try:
        subprocess.run(
            [find_browser(), "--headless=new", "--disable-gpu", "--no-sandbox", "--allow-file-access-from-files",
             "--virtual-time-budget=15000", f"--print-to-pdf={pdf_path}", html_path.as_uri()],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120,
        )
    finally:
        html_path.unlink(missing_ok=True)
    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        raise RuntimeError(f"PDF was not created: {pdf_path}")
    return pdf_path


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    for arg in sys.argv[1:]:
        md_path = Path(arg).resolve()
        if md_path.suffix.lower() != ".md" or not md_path.is_file():
            print(f"skip: {arg} (not an existing .md file)", file=sys.stderr)
            continue
        print(export(md_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
