---
name: cli
description: 使用 CLI 工具（glab、kubectl、gcloud、bq、aws 等）處理其輸出時觸發。核心規則：解析／篩選 CLI 的 JSON 輸出用 jq，不用 Python。
user-invocable: true
---

## 操作前說明與確認

執行 CLI 指令前，先用中文簡要說明用途。遇到破壞性操作（刪除、合併、關閉、強制推送、改雲端資源）或費用不低的操作（如 `bq query` 依掃描量計費、觸發 workflow／scheduled query 等運算），先告知使用者並等確認才執行。免費的 metadata 讀取（`... list`、`bq show`/`ls`、讀 config、`glab api` 讀檔等）可直接執行。

## CLI JSON 解析：用 jq，不用 Python

處理 CLI 工具的 JSON 輸出時，用 `jq` 在管道中完成篩選與轉換，不要寫 Python 腳本

多數 CLI 支援 `--output json` / `-o json` / `--format json`；若子命令不支援 JSON，通知使用者，由使用者決定怎麼處理。

**不用 jq 的情況**：任務已超出「篩選 JSON」的範疇
