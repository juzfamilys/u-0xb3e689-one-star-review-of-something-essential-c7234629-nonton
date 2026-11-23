#!/usr/bin/env python3
"""One-Star Review of Something Essential.

Writes a single deadpan one-star review of sleep to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

Pure Python standard library only. Deterministic: the same bytes
on every run.
"""

import os
import sys

# The review: a deadpan one-star complaint filed in earnest against
# sleep, an everyday essential that cannot be fixed. The grievance is
# the small nightly annoyance everyone recognises -- paying for eight
# hours of rest and receiving a 4am review of every mistake instead --
# and the sting lands in the last few words.
ENTRY = (
    "Advertised eight hours of rest. Delivered three hours of "
    "ceiling-staring and a 4am review of every mistake I have ever made."
)

MAX_CHARS = 160


def validate(text):
    """Enforce the competition gate: 1-160 chars, one line, real text."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            "entry must be 1 to %d characters, got %d" % (MAX_CHARS, len(text))
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing white space")
    if "!" in text:
        # Deadpan guard: the judge's brief says no exclamation marks
        # doing the work. A one-star review must stay flat.
        raise ValueError("entry must not contain exclamation marks")
    return text


def main():
    validate(ENTRY)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    # No trailing newline: the file is exactly the review, nothing else.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    with open(path, "rb") as f:
        written = f.read()
    if written.decode("utf-8") != ENTRY:
        raise ValueError("round-trip check failed: file differs from ENTRY")
    validate(written.decode("utf-8"))
    print("wrote %d characters to %s" % (len(ENTRY), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
