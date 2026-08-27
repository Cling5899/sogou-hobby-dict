# 搜狗个人词库

面向搜狗拼音的爱好向中文词库：曼城 / 英超球员译名，以及自行车赛事、车手译名（偏波加查赛历）。

源数据是 UTF-8 YAML，构建脚本导出搜狗可导入的 GBK 文本词库。打拼音出整词（`halande` → 哈兰德），不做英文缩写短语。

## 快速开始

```bash
pip install -r requirements.txt
python scripts/build.py
```

生成：

| 文件 | 用途 |
| --- | --- |
| 桌面 `sogou_all.txt` | 导入搜狗（推荐，英文路径） |
| `dist/gbk/sogou_all.txt` | 同上，留在仓库里 |
| `dist/gbk/sogou_smoke.txt` | 只有 3 词，导入失败时先测这个 |
| `dist/utf8/*.txt` | Git 对照，不要拿去导入 |

导入步骤见 [docs/import-sogou.md](docs/import-sogou.md)。若提示「导入词库失败」，多半是换行/间隔号/超长词，重新 `python scripts/build.py` 后再导桌面那份。

## 加词

编辑 `sources/football.yaml` 或 `sources/cycling.yaml`：

```yaml
- word: 哈兰德
  pinyin: ha lan de
  aliases: [埃尔林·哈兰德]
  tags: [mancity, current]
  source: 中文维基
```

译名以中文维基常用写法为准，不要自造。YAML 可以写间隔号；导入文件会去掉符号并限制 2–10 个汉字。然后重新 `python scripts/build.py`，再导入桌面上的 `sogou_all.txt`。

## 官方 scel

若有搜狗官网的 `足球【官方推荐】.scel`，放到 `vendor/` 后：

```bash
python scripts/parse_scel.py vendor/足球【官方推荐】.scel
```

只作对照，有用的词再并入 YAML。本仓库**不生成** `.scel`。

## Cursor Skill

- 项目内：`.cursor/skills/sogou-hobby-dict/SKILL.md`
- 本机跨项目：`~/.cursor/skills/sogou-hobby-dict/`

提到搜狗、词库、曼城译名、波加查、环法、scel 时按该 Skill 维护词库。
