---
name: sogou-hobby-dict
description: >-
  Maintain a personal Sogou IME dictionary for Manchester City, Premier League,
  and cycling (Pogacar) Chinese names. Use when the user mentions 搜狗, 词库,
  译名, 曼城, 英超, 波加查, 环法, 自行车, scel, or adding player/race names for typing.
---

# 搜狗个人词库

Default data dir: `C:\Users\Admin\Desktop\个人词库`. If the current workspace is a clone of this repo, use the workspace root.

## Always

1. Read `sources/football.yaml` and `sources/cycling.yaml` before changing words.
2. Prefer 中文维基常用译名. Do not invent translations.
3. After YAML edits, run `python scripts/build.py` from the repo root.
4. Tell the user to re-import Desktop `sogou_all.txt` (ASCII path). Do not claim the IME was updated automatically.

## Add a word

Look up 中文维基 (or club / UAE Team Chinese site). Append:

```yaml
- word: 哈兰德
  pinyin: ha lan de
  aliases: [埃尔林·哈兰德]
  tags: [mancity, current]
  source: 中文维基
```

- `aliases` export as separate lines.
- Use ASCII hyphen `-`, not en-dash, so GBK import works.
- tags: `mancity` `current` `historic` `coach` `club` `competition` `rider` `race` `team`

## Update squad / calendar

Only edit the matching YAML section. Move leavers from `current` to `historic`. Rebuild.

## Parse official scel

If the user drops `*.scel` into `vendor/`:

```
python scripts/parse_scel.py vendor/足球【官方推荐】.scel
```

Merge useful words into YAML by hand. Do not dump scel output straight into dist.

## Do not

- Generate `.scel` (not reliably possible)
- Write English-shortcut phrases (`haaland,1=哈兰德`)
- Edit Sogou install / user AppData
- Add encyclopedic lists beyond 曼城/英超专名 and 自行车一线车手/赛事

## After

Say what was added or moved, print rebuild counts, and remind: 搜狗 → 词库 → 导入文本词库 → 桌面 `sogou_all.txt`。 If import fails, try `dist/gbk/sogou_smoke.txt` first.
