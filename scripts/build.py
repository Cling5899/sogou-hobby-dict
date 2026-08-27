#!/usr/bin/env python3
"""Build Sogou importable dictionaries from sources/*.yaml."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Need PyYAML: pip install -r requirements.txt")

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"
DIST_UTF8 = ROOT / "dist" / "utf8"
DIST_GBK = ROOT / "dist" / "gbk"

FILE_MAP = {
    "football.yaml": "足球_曼城.txt",
    "cycling.yaml": "自行车.txt",
}


def load_words(path: Path) -> list[str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    words: list[str] = []
    seen: set[str] = set()
    for entry in data.get("entries") or []:
        candidates = [entry.get("word"), *(entry.get("aliases") or [])]
        for raw in candidates:
            if not raw:
                continue
            word = str(raw).strip()
            if word and word not in seen:
                seen.add(word)
                words.append(word)
    return words


def write_utf8(path: Path, words: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(words) + "\n", encoding="utf-8")


def write_gbk(path: Path, words: list[str]) -> list[str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    ok: list[str] = []
    skipped: list[str] = []
    for word in words:
        try:
            word.encode("gbk")
            ok.append(word)
        except UnicodeEncodeError:
            skipped.append(word)
    path.write_bytes(("\n".join(ok) + "\n").encode("gbk"))
    return skipped


def main() -> None:
    all_words: list[str] = []
    all_seen: set[str] = set()
    for src_name, out_name in FILE_MAP.items():
        src = SOURCES / src_name
        if not src.exists():
            sys.exit(f"missing {src}")
        words = load_words(src)
        write_utf8(DIST_UTF8 / out_name, words)
        skipped = write_gbk(DIST_GBK / out_name, words)
        print(f"{src_name}: {len(words)} words -> {out_name}")
        if skipped:
            print(f"  GBK skipped: {skipped}")
        for word in words:
            if word not in all_seen:
                all_seen.add(word)
                all_words.append(word)
    write_utf8(DIST_UTF8 / "全部.txt", all_words)
    skipped = write_gbk(DIST_GBK / "全部.txt", all_words)
    print(f"all: {len(all_words)} words")
    if skipped:
        print(f"  GBK skipped: {skipped}")


if __name__ == "__main__":
    main()
