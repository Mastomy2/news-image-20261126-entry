#!/usr/bin/env python3
"""Entry runner for the make.fun news-image-20261126 bounty.

Validates the poster ``image.png`` next to this file (PNG signature,
IHDR chunk, exactly 1024x1024, at most 1 MiB) and copies it to
``entry.png`` inside the output directory (``$MAKEFUN_OUTPUT_DIR``,
or ``/output`` by default). The poster itself is drawn by
``draw_poster.py`` in this same directory; this runner only
validates the PNG and copies it, so the graded bytes are exactly
the bytes the drawing program produced.

Prints the output path, SHA-256 and size of the copied file, and
verifies the copy byte-for-byte by re-hashing it after the write.
Exits non-zero if anything fails to validate.

Standard library only. Python 3.13. The copy is byte-for-byte
deterministic: the same image.png always produces the same entry.png,
so the program's two grader runs write identical bytes.
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

MAX_BYTES = 1024 * 1024  # 1 MiB, the bounty cap in RULES.txt
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("error: " + message, file=sys.stderr)
    sys.exit(1)


def check_png(data):
    """Validate PNG bytes; return (width, height) or exit 1."""
    if len(data) < 33:
        fail("image.png is too small to be a PNG (%d bytes)" % len(data))
    if data[:8] != PNG_SIGNATURE:
        fail("image.png is not a PNG file (bad signature)")
    if data[12:16] != b"IHDR":
        fail("image.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        fail("image.png is %dx%d, expected 1024x1024" % (width, height))
    return width, height


def main():
    here = Path(__file__).resolve().parent
    src = here / "image.png"
    if not src.is_file():
        fail("image.png not found next to main.py")

    try:
        data = src.read_bytes()
    except OSError as exc:
        fail("cannot read image.png: %s" % exc)

    if len(data) > MAX_BYTES:
        fail("image.png is %d bytes, over the 1 MiB limit" % len(data))
    if len(data) == 0:
        fail("image.png is empty")

    width, height = check_png(data)
    digest = hashlib.sha256(data).hexdigest()

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "entry.png"
        out_path.write_bytes(data)
    except OSError as exc:
        fail("cannot write entry.png: %s" % exc)

    if hashlib.sha256(out_path.read_bytes()).hexdigest() != digest:
        fail("entry.png hash mismatch after copy")

    print("output: %s" % out_path)
    print("entry.png sha256=%s size=%d bytes %dx%d OK"
          % (digest, len(data), width, height))


if __name__ == "__main__":
    main()
