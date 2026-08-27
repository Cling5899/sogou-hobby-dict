#!/usr/bin/env python3
"""Extract Chinese words from a Sogou .scel cell dictionary."""

from __future__ import annotations

import struct
import sys
from pathlib import Path


def parse_scel(path: Path) -> list[str]:
    data = path.read_bytes()
    if len(data) < 0x2628:
        raise ValueError(f"too small to be scel: {path}")

    hz_offset = 0x2628
    mask = struct.unpack_from("<H", data, 0x120)[0]
    if mask == 0x45:
        hz_offset = 0x26C4

    words: list[str] = []
    i = hz_offset
    end = len(data)
    while i + 4 <= end:
        same = struct.unpack_from("<H", data, i)[0]
        i += 2
        py_bytes = struct.unpack_from("<H", data, i)[0]
        i += 2
        if py_bytes > end - i:
            break
        i += py_bytes
        for _ in range(same):
            if i + 2 > end:
                return words
            word_len = struct.unpack_from("<H", data, i)[0]
            i += 2
            if word_len <= 0 or i + word_len > end:
                return words
            word = data[i : i + word_len].decode("utf-16-le", errors="ignore").strip()
            i += word_len
            if i + 2 > end:
                return words
            ext_len = struct.unpack_from("<H", data, i)[0]
            i += 2
            if i + ext_len > end:
                return words
            i += ext_len
            if word:
                words.append(word)
    return words


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: python scripts/parse_scel.py vendor/foo.scel [out.txt]")
    src = Path(sys.argv[1])
    if not src.is_file():
        sys.exit(f"not found: {src}")
    words = parse_scel(src)
    # keep order, drop duplicates
    unique: list[str] = []
    seen: set[str] = set()
    for word in words:
        if word not in seen:
            seen.add(word)
            unique.append(word)
    text = "\n".join(unique) + "\n"
    if len(sys.argv) >= 3:
        Path(sys.argv[2]).write_text(text, encoding="utf-8")
        print(f"{len(unique)} words -> {sys.argv[2]}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(text)
        print(f"# {len(unique)} words", file=sys.stderr)


if __name__ == "__main__":
    main()
