#!/usr/bin/env python3
"""Build Sogou importable dictionaries from sources/*.yaml."""

from __future__ import annotations

import re
import shutil
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
DESKTOP = Path.home() / "Desktop"

FILE_MAP = {
    "football.yaml": ("足球_曼城.txt", "sogou_football.txt"),
    "cycling.yaml": ("自行车.txt", "sogou_cycling.txt"),
}

# New Sogou text import: CRLF, ANSI/GBK, one word per line, 2-10 Han chars, no punctuation.
SOGOU_WORD = re.compile(r"^[\u4e00-\u9fff]{2,10}$")
STRIP_CHARS = str.maketrans("", "", "·•・．.－—–-/\\()[]{}")


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


def sogou_word(word: str) -> str | None:
    cleaned = word.translate(STRIP_CHARS).strip()
    if SOGOU_WORD.fullmatch(cleaned):
        return cleaned
    return None


def to_sogou_words(words: list[str]) -> tuple[list[str], list[str]]:
    out: list[str] = []
    seen: set[str] = set()
    skipped: list[str] = []
    for word in words:
        cleaned = sogou_word(word)
        if cleaned is None:
            skipped.append(word)
            continue
        if cleaned not in seen:
            seen.add(cleaned)
            out.append(cleaned)
    return out, skipped


def write_utf8(path: Path, words: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(words) + "\n", encoding="utf-8")


def write_gbk(path: Path, words: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = "\r\n".join(words) + "\r\n"
    path.write_bytes(body.encode("gbk"))


def emit_gbk(words: list[str], chinese_name: str, ascii_name: str) -> None:
    write_gbk(DIST_GBK / chinese_name, words)
    write_gbk(DIST_GBK / ascii_name, words)


def main() -> None:
    all_raw: list[str] = []
    all_seen: set[str] = set()
    for src_name, (cn_name, ascii_name) in FILE_MAP.items():
        src = SOURCES / src_name
        if not src.exists():
            sys.exit(f"missing {src}")
        raw = load_words(src)
        write_utf8(DIST_UTF8 / cn_name, raw)
        words, skipped = to_sogou_words(raw)
        emit_gbk(words, cn_name, ascii_name)
        print(f"{src_name}: {len(raw)} source -> {len(words)} sogou")
        if skipped:
            print(f"  skipped: {', '.join(skipped)}")
        for word in raw:
            if word not in all_seen:
                all_seen.add(word)
                all_raw.append(word)

    write_utf8(DIST_UTF8 / "全部.txt", all_raw)
    all_words, skipped = to_sogou_words(all_raw)
    emit_gbk(all_words, "全部.txt", "sogou_all.txt")
    write_gbk(DIST_GBK / "sogou_smoke.txt", ["哈兰德", "环法", "波加查"])
    desktop_copy = DESKTOP / "sogou_all.txt"
    shutil.copyfile(DIST_GBK / "sogou_all.txt", desktop_copy)
    print(f"all: {len(all_raw)} source -> {len(all_words)} sogou")
    if skipped:
        print(f"  skipped: {', '.join(skipped)}")
    print(f"import: {desktop_copy}")


if __name__ == "__main__":
    main()
