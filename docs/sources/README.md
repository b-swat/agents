# docs/sources — Source Documents

Datasheets, reference manuals, standards, customer requirements, schematics.

- Read-only for both agents; files are added by the lead. **Local only — agents never search the internet;**
  a missing datasheet is requested from the lead.
- File name: `<vendor>_<document>_<revision>.<ext>`, e.g. `ST_RM0090_rev19.pdf`.
- Source documents may be in any language and format (PDF, DOCX, etc.).
  Everything derived from them is English Markdown.
- ChatGPT's English translations are placed next to the original with suffix `_en`:
  `Vendor_Spec_rev2_en.md`.
- When a document is updated, the old revision is kept — specs may reference it.
