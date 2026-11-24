#!/usr/bin/env python3
"""news-23 b93 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import binascii
import hashlib
import os
import struct
import sys

SRC_NAME = "entry.png"
EXPECTED_W, EXPECTED_H = 1024, 1024
MIN_BYTES = 10_000
MAX_BYTES = 1_048_576


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def read_png_header(path):
    """Parse the PNG header manually (struct only) and walk chunks.

    Returns (width, height, total_idat_payload, sha256_hex).
    """
    with open(path, "rb") as f:
        data = f.read()
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("bad PNG signature")
    if len(data) > MAX_BYTES:
        fail(f"entry.png too large: {len(data)} bytes (max {MAX_BYTES})")
    if len(data) < MIN_BYTES:
        fail(f"entry.png too small: {len(data)} bytes (min {MIN_BYTES})")
    off = 8
    first = True
    total_idat = 0
    last_type = None
    while off + 8 <= len(data):
        (length,) = struct.unpack(">I", data[off:off + 4])
        ctype = data[off + 4:off + 8]
        if off + 12 + length > len(data):
            fail(f"truncated chunk {ctype!r}")
        chunk_data = data[off + 8:off + 8 + length]
        (crc_stored,) = struct.unpack(">I", data[off + 8 + length:off + 12 + length])
        crc_calc = binascii.crc32(ctype)
        crc_calc = binascii.crc32(chunk_data, crc_calc) & 0xFFFFFFFF
        if crc_calc != crc_stored:
            fail(f"bad CRC in chunk {ctype!r}")
        if first:
            if ctype != b"IHDR" or length != 13:
                fail("first chunk must be a 13-byte IHDR")
            w, h, depth, ctype_col, comp, filt, inter = struct.unpack(">IIBBBBB", chunk_data)
            if (w, h) != (EXPECTED_W, EXPECTED_H):
                fail(f"bad dimensions: {w}x{h} (want {EXPECTED_W}x{EXPECTED_H})")
            if depth != 8 or ctype_col not in (2, 6):
                fail(f"bad IHDR: bit depth {depth}, colour type {ctype_col}")
            if (comp, filt, inter) != (0, 0, 0):
                fail(f"bad IHDR: compression {comp}, filter {filt}, interlace {inter}")
            first = False
        if ctype == b"IDAT":
            if length == 0:
                fail("empty IDAT chunk")
            total_idat += length
        last_type = ctype
        off += 12 + length
        if ctype == b"IEND":
            break
    if first:
        fail("missing IHDR")
    if last_type != b"IEND":
        fail("missing IEND as final chunk")
    if off != len(data):
        fail("trailing data after IEND")
    if total_idat < 1000:
        fail(f"IDAT payload too small: {total_idat} bytes")
    return hashlib.sha256(data).hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    if not os.path.isfile(src):
        fail(f"{SRC_NAME} not found next to main.py")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir = os.path.abspath(out_dir)
    here_real = os.path.realpath(here)
    out_real = os.path.realpath(out_dir)
    if os.path.exists(out_real) and not os.path.isdir(out_real):
        fail("MAKEFUN_OUTPUT_DIR is a file, not a directory")
    if out_real == here_real or out_real.startswith(here_real + os.sep):
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repo (grader runs read-only)")
    sha = read_png_header(src)
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, SRC_NAME)
    if os.path.realpath(dst) == os.path.realpath(src):
        fail("output would overwrite the source entry.png")
    with open(src, "rb") as f:
        blob = f.read()
    with open(dst, "wb") as f:
        f.write(blob)
    with open(dst, "rb") as f:
        check = f.read()
    if check != blob:
        fail("output is not byte-identical to source")
    print(f"wrote {dst} ({len(blob)} bytes, sha256 {sha})")


if __name__ == "__main__":
    main()
