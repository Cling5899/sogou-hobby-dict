# 导入搜狗输入法

本仓库生成的是**用户文本词库**，不是 `.scel` 细胞词库。

新版搜狗对 txt 很挑：整份文件有一行不合格，就会提示「导入词库失败！请稍后重试。」

## 用哪个文件

优先导入**英文路径**这份（构建脚本会复制到桌面）：

- `C:\Users\Admin\Desktop\sogou_all.txt`

或仓库内：

- `dist/gbk/sogou_all.txt`

不要用 `dist/utf8/`，也不要直接拿带间隔号 `·` 的对照文件去导。

## 步骤

1. 仓库根目录运行 `python scripts/build.py`（会刷新桌面上的 `sogou_all.txt`）。
2. 右键搜狗状态栏 → **设置属性** → **词库** → **导入文本词库**。
3. 选桌面上的 `sogou_all.txt`。文件类型选「文本词库（*.txt）」。
4. 到任意输入框打 `halande`、`huanfa`、`bogacha`。

若整份仍失败，先导入 `dist/gbk/sogou_smoke.txt`（只有 3 个词）。烟测能过、全量不过，把报错发回来。

## 格式（构建脚本已处理）

- ANSI/GBK，Windows 换行 CRLF
- 一行一个词，纯汉字，2–10 字
- 去掉间隔号、连字符、英文（`B席`、`UCI…` 等不会进导入文件）

YAML 里仍保留带 `·` 的全名，方便对照。

## 更新词库后

重新 `python scripts/build.py`，再在搜狗里导入一次桌面上的 `sogou_all.txt`。本流程不会自动写入输入法。
