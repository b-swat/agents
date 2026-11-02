---
name: export-pdf
description: Export a Markdown document (task spec) with Mermaid diagrams to a PDF copy next to it, offline, on macOS and Ubuntu. Use after every change of a task spec in docs/tasks/ or when the lead asks for a PDF.
---

# export-pdf — Markdown → PDF export copy

The `.md` is the source of truth; the `.pdf` next to it is only an export copy (AGENTS.md, section 0.1).
Never edit the PDF and never use it as input.

## Command

```sh
python3 .claude/skills/export-pdf/md2pdf.py docs/tasks/YYYY-MM-DD-<task-name>.md [more.md ...]
```

Output: `docs/tasks/YYYY-MM-DD-<task-name>.pdf` (same folder, same base name); the script prints its path.

## How it works

1. `markdown-it-py` renders Markdown (tables, code) to HTML; raw HTML in the source is escaped, HTML comments are dropped.
2. ` ```mermaid ` blocks are rendered by the local copy `vendor/mermaid.min.js` (mermaid 10.9.1) — no internet needed.
3. Headless Chrome / Chromium / Edge prints the page to A4 PDF (header: file name + version, footer: page numbers).

## Prerequisites

| | Ubuntu | macOS |
|---|---|---|
| Python 3 | `sudo apt install python3 python3-pip` | `brew install python` (or Xcode CLT) |
| markdown-it-py | `python3 -m pip install markdown-it-py` | `python3 -m pip install markdown-it-py` |
| Browser | Google Chrome (`google-chrome`) or `chromium` | Google Chrome / Chromium / Edge in `/Applications` |

Browser override: `MD2PDF_BROWSER=/path/to/browser`.

## Checking the result

- Exit code 0 and a printed `.pdf` path.
- Optional visual check (pypdfium2 is available on the dev machine):
  `python3 -c "import pypdfium2 as p; d=p.PdfDocument('<file>.pdf'); print(len(d), 'pages')"`.
- A raw Mermaid source in the PDF text (e.g. the word `flowchart`) means the diagram did not render — check the
  diagram syntax in the `.md`.

## Known problems

- Very tall diagrams are scaled to fit one page (max height 235 mm); split them if text gets too small.
- Text in angle brackets (`<TAG>`) is shown literally — raw HTML is not supported by design.
- Verified on Ubuntu with Google Chrome 156 (2026-11-02). macOS path detection is implemented but not yet run on a Mac —
  on the first macOS run, verify and record the result here.
