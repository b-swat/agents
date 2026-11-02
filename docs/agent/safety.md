# Prohibitions and Actions Requiring Confirmation

> Status: **draft** — the lead will extend it.

## Only With Explicit Confirmation From the Lead [ASSUMPTION]

- Flashing the device, erasing Flash, writing option bytes / fuses / OTP.
- Changing linker scripts, startup code, clock configuration.
- Changing generated code (CubeMX, etc.) and third-party libraries.
- Deleting files, large-scale refactoring.
- Any git operation that rewrites history or touches a remote repository (push, fetch, pull included).
- Resolving merge conflicts in `development`.
- Implementation before the development plan is approved; adding or changing tests before the lead confirms them.
- Changing requirements, plan or tests of an approved task spec.
- Adding any document (README, design notes, `.md` files, etc.) to a project repository.

## Prohibited

- Editing files in `docs/sources/`.
- Searching the internet for datasheets, documentation or tools — ask the lead instead.
- Editing a PDF export or using it as input; the `.md` is the source.
- Presenting unverified results as verified.
- Creating documents in any language other than English or in any format other than Markdown.
- Editing or deleting existing entries in the "Change History" / "Decisions" sections of
  `MEMORY.md` and `MEMORY_REL.md` (append-only; see AGENTS.md, section 6).
- Placing working or temporary documents (reports, questions, memory, notes, logs) inside a repository —
  they belong in the working directory (AGENTS.md, section 0.2).

## Protected Files and Directories

TBD
