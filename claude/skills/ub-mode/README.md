# ub-mode

來源：[Uncle Bob 的 ub-mode](https://github.com/unclebob/ub-mode)。

此版本已刪除 `SKILL.md` 中整個 `Practice` 區塊。

## 安裝工具（macOS／Linux）

先安裝 [uv](https://docs.astral.sh/uv/getting-started/installation/)，再於此目錄執行：

```sh
uv run install.py
```

每次執行都會下載三個工具最新的預設分支版本。

從要分析的專案目錄執行（將路徑換成此 skill 的實際位置）：

```sh
uv run /path/to/ub-mode/run.py crapper --help
uv run /path/to/ub-mode/run.py dryer --help
uv run /path/to/ub-mode/run.py mutator --help
```

專案本身的測試與覆蓋率工具仍需另行設定。

## Codex 執行 crapper（macOS）

從目標專案根目錄執行，替換 skill 路徑與待分析檔案：

```sh
UV_CACHE_DIR=/private/tmp/ub-mode-uv \
TREE_SITTER_LANGUAGE_PACK_CACHE_DIR=/private/tmp/ub-mode-parsers \
uv run /path/to/ub-mode/run.py crapper \
  --root /private/tmp/ub-mode-report \
  /absolute/path/to/project/src/example.js
```

此範例將 `--root` 設為暫存報告目錄，因此待分析檔案須使用絕對路徑；相對路徑會以 `--root` 為基準解析，而非目前工作目錄。
