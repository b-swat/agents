#!/usr/bin/env python3
"""Check the strict format of the "Test Procedure" and "Re-test Log" sections of a task spec.

Usage: check_test_procedure.py docs/tasks/YYYY-MM-DD-<task-name>.md
Exit code 0 — format OK; 1 — errors (printed). Format: docs/agent/testing.md, "Test Procedure format".
Works on macOS and Ubuntu (stdlib only).
"""
import re
import sys
from pathlib import Path

ENV_ROWS = ["OS", "Repository", "Branch", "Commit", "Compiler", "CMake", "GoogleTest", "Other tools"]
SUBSECTIONS = ["Environment", "Prerequisites", "Steps", "Test Results", "Summary"]
STEP_FIELDS = ["- Working directory:", "- Command:", "- Expected:", "- Pass criterion:"]
PLACEHOLDER = re.compile(r"<[A-Za-z][^<>]*>|YYYY-MM-DD")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TEST_NAME = re.compile(r"^`?\w+\.REQ_[A-Z0-9]+_\d{2}_\w+`?$")
REQ_ID = re.compile(r"^REQ-[A-Z0-9]+-\d{2}$")

errors = []


def section(text, title):
    m = re.search(rf"^## (\d+)\. {re.escape(title)}\b.*$", text, re.MULTILINE)
    if not m:
        return None, None
    end = re.search(r"^## \d+\. ", text[m.end():], re.MULTILINE)
    return m.group(1), text[m.end(): m.end() + end.start() if end else len(text)]


def subsection(body, num, title):
    m = re.search(rf"^### {num}\.\d+ {re.escape(title)}\s*$", body, re.MULTILINE)
    if not m:
        errors.append(f"missing subsection '### {num}.x {title}'")
        return ""
    end = re.search(r"^### ", body[m.end():], re.MULTILINE)
    return body[m.end(): m.end() + end.start() if end else len(body)]


def table_rows(block):
    rows = [l.strip() for l in block.splitlines() if l.strip().startswith("|")]
    cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
    return [c for c in cells[2:]] if len(cells) >= 2 else []


def no_placeholder(where, value):
    if PLACEHOLDER.search(value):
        errors.append(f"{where}: unfilled placeholder in '{value}'")


def check(text):
    num, body = section(text, "Test Procedure")
    if body is None:
        errors.append("missing section '## N. Test Procedure'")
        return

    env = {r[0]: r[1] for r in table_rows(subsection(body, num, "Environment")) if len(r) >= 2}
    for row in ENV_ROWS:
        if not env.get(row):
            errors.append(f"Environment: missing or empty row '{row}'")
        else:
            no_placeholder(f"Environment/{row}", env[row])

    prereq = table_rows(subsection(body, num, "Prerequisites"))
    if not prereq:
        errors.append("Prerequisites: table has no rows (write 'none' if nothing is needed)")
    for r in prereq:
        if len(r) != 3:
            errors.append(f"Prerequisites: row must have 3 columns (#, Ubuntu, macOS): {r}")
        no_placeholder("Prerequisites", " ".join(r))

    steps_block = subsection(body, num, "Steps")
    steps = re.split(r"^#### ", steps_block, flags=re.MULTILINE)[1:]
    if not steps:
        errors.append("Steps: no '#### STEP-NN: <title>' entries")
    for i, step in enumerate(steps, 1):
        head = step.splitlines()[0]
        if not re.match(rf"^STEP-{i:02d}: \S", head):
            errors.append(f"Steps: expected heading 'STEP-{i:02d}: <title>', got '{head}'")
        for field in STEP_FIELDS:
            if not re.search(rf"^{re.escape(field)}", step, re.MULTILINE):
                errors.append(f"STEP-{i:02d}: missing field '{field}'")
        if not re.search(r"^```sh\n.+?\n```", step, re.MULTILINE | re.DOTALL):
            errors.append(f"STEP-{i:02d}: command must be a non-empty ```sh block")
        no_placeholder(f"STEP-{i:02d}", step)

    results = table_rows(subsection(body, num, "Test Results"))
    if not results:
        errors.append("Test Results: no rows")
    for r in results:
        if len(r) != 5:
            errors.append(f"Test Results: row must have 5 columns: {r}")
            continue
        test, req, result, date, by = r
        if not TEST_NAME.match(test):
            errors.append(f"Test Results: test name '{test}' must be Suite.REQ_<TAG>_<NN>_<Behavior>")
        if not REQ_ID.match(req):
            errors.append(f"Test Results: '{req}' is not REQ-<TAG>-<NN>")
        if result not in ("pass", "fail", "skip"):
            errors.append(f"Test Results: result '{result}' must be pass/fail/skip")
        if not DATE.match(date):
            errors.append(f"Test Results: date '{date}' must be YYYY-MM-DD")
        if not by:
            errors.append("Test Results: 'Run by' is empty")

    summary = table_rows(subsection(body, num, "Summary"))
    if len(summary) != 1 or len(summary[0]) != 7:
        errors.append("Summary: exactly one row with 7 columns required")
    else:
        total, passed, failed, skipped, suite, date, _ = summary[0]
        try:
            t, p, f, s = map(int, (total, passed, failed, skipped))
            if t != p + f + s:
                errors.append("Summary: Total != Passed + Failed + Skipped")
            if t != len(results):
                errors.append(f"Summary: Total {t} != {len(results)} rows in Test Results")
            if f == 0 and suite != "pass" or f > 0 and suite != "fail":
                errors.append("Summary: 'Full suite' must be 'fail' if any test failed, else 'pass'")
        except ValueError:
            errors.append("Summary: Total/Passed/Failed/Skipped must be integers")
        if not DATE.match(date):
            errors.append(f"Summary: date '{date}' must be YYYY-MM-DD")

    _, log = section(text, "Re-test Log")
    if log is None:
        errors.append("missing section '## N. Re-test Log'")
        return
    for r in table_rows(log):
        if all(c in ("—", "-", "") for c in r):
            continue  # "no re-test yet"
        if len(r) != 8:
            errors.append(f"Re-test Log: row must have 8 columns: {r}")
            continue
        if not re.match(r"^R-\d{2}$", r[0]):
            errors.append(f"Re-test Log: run ID '{r[0]}' must be R-NN")
        if not DATE.match(r[1]):
            errors.append(f"Re-test Log: date '{r[1]}' must be YYYY-MM-DD")
        if r[6] not in ("pass", "fail"):
            errors.append(f"Re-test Log: result '{r[6]}' must be pass/fail")


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    check(Path(sys.argv[1]).read_text(encoding="utf-8"))
    for e in errors:
        print(f"ERROR: {e}")
    print("Test Procedure format: " + ("OK" if not errors else f"{len(errors)} error(s)"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
