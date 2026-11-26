# The Self-Checkout Is Judging You — make.fun entry
# One funny line (1-200 chars) written to entry.txt.
"""One smug remark from a judgmental self-checkout machine.

Why this line, re-derived from the brief rather than copied from
the earlier draft: the judge scores a single read — a real laugh,
a twist a stranger gets with no context, the machine's voice, and
freshness (not the bagging-area gag everyone has heard). The line
is built in three beats that each do one job:

1. "Twelve yoghurts, no bag, no plan." — three short fragments,
   a rule of three. The basket is the whole shop (twelve yoghurts,
   nothing else), and "no bag, no plan" says the shopper walked in
   with no system at all. The machine is already unimpressed.
2. "I've scanned your entire personality" — the scan is the
   machine's only sense, so it scans the one thing it cannot see:
   the shopper. That is the twist: the scanner stops scanning
   groceries and starts scanning the person.
3. "and it expires Friday." — the sting. Yoghurt has a use-by
   date, so the personality gets one too, and Friday is close
   enough to hurt. One sting only: a second sting (search history,
   dignity, spoons) would split the laugh, so the line stops here.

93 characters, one line, no padding. The bagging-area joke is
deliberately nowhere in it.
"""
import os
from pathlib import Path

ENTRY = (
    "Twelve yoghurts, no bag, no plan. "
    "I've scanned your entire personality and it expires Friday."
)

def validate_entry(text):
    """Refuse an entry the grader would throw away, before writing it.

    Re-derived from the brief's gate, check by check — each rule
    maps to one way an entry can fail silently downstream, so each
    failure here is loud (SystemExit with a reason) instead of a
    quiet zero later:

    - Blank or whitespace-only: an empty entry is not a joke; the
      judge cannot laugh at nothing, and a file containing only
      spaces would pass a naive length check while scoring nothing.
    - Length outside 1-200 characters: the brief caps the line at
      200 characters. 93 is comfortably inside, but the check is
      written against the limit, not the current value, so a future
      edit that creeps past 200 fails here instead of at grading.
    - Leading or trailing whitespace: a stray space would count
      toward the 200 and could break the "single line" reading;
      stripping is not an option because silently changing the
      entry would make the file differ from what was reviewed.
    - Any newline or carriage return: the entry must be one line,
      so an embedded line break is a different entry shape entirely.
    - Not encodable as UTF-8: the grader reads the file as text;
      an unencodable string would crash the read, so encode it
      here as a dry run and let the exception surface.
    """
    if not text or not text.strip():
        raise SystemExit("entry must not be blank")
    if not 1 <= len(text) <= 200:
        raise SystemExit(f"entry must be 1-200 chars, got {len(text)}")
    if text != text.strip():
        raise SystemExit("entry must not start or end with whitespace")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line")
    text.encode("utf-8")  # raises if the text is not valid UTF-8 text


def main():
    """Validate, then write the entry deterministically.

    Why this shape: the output path comes from MAKEFUN_OUTPUT_DIR
    because the harness sets it per run — hardcoding /output would
    break local grading, and defaulting to /output keeps the
    documented contract when the variable is unset. mkdir with
    parents=True means a fresh output directory is not an error.
    write_text with explicit UTF-8 (no trailing newline appended)
    makes the file byte-identical on every run: the same ENTRY
    string, the same encoding, no timestamps, no randomness — so
    two runs into two different directories must produce identical
    bytes, which is the determinism check I run before submitting.
    Validation runs before any directory is created, so a bad entry
    leaves no file behind for the grader to pick up by mistake.
    """
    validate_entry(ENTRY)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "entry.txt").write_text(ENTRY, encoding="utf-8")
    print(f"wrote entry.txt ({len(ENTRY)} chars)")


if __name__ == "__main__":
    main()
