---
name: cli
description: 使用 CLI 工具（glab、kubectl、gcloud、bq、aws 等）時的解析規則。當任務涉及 CLI 指令輸出的解析、篩選或轉換時，必須使用 jq 而非 Python。無論使用者是否明確提到 jq，只要涉及 CLI JSON 輸出處理就應觸發此 skill。
user-invocable: true
---

# CLI JSON 解析：用 jq，不用 Python

當使用者要查詢、篩選、統計來自 CLI 工具的資料時，用 `jq` 直接在管道中完成。不要寫 Python 腳本——jq 一行就能解決，使用者可以直接複製貼上到自己的終端機重現，不需要額外的 runtime 或檔案。

這個選擇背後的原因：使用者在終端機操作 CLI 時，期望的是快速、可組合的管道指令。一個 jq one-liner 比一段 Python 腳本更容易理解、修改、和分享給同事。

## 做法

1. **優先取得 JSON 輸出**——大多數 CLI 都支援 `--output json`、`-o json`、`--format json` 等旗標。先拿到乾淨的 JSON，再用 jq 處理
2. **若子命令不支援 JSON**，改用對應的 API endpoint（`glab api`、`curl`）或工具內建的查詢功能（如 `bq --format=json`）
3. **即使轉換較複雜**（排序、分組、統計、多欄位重組），也用 jq 完成。jq 的 `group_by`、`sort_by`、`@tsv`、`@csv` 等功能足以應付絕大多數場景
4. **表格輸出**用 `jq -r '... | @tsv'` 搭配 `column -t`

## 範例

標準 pipe 模式：

```bash
kubectl get pods -o json | jq '.items[] | select(.status.phase != "Running") | {name: .metadata.name, phase: .status.phase}'
glab mr list --output json | jq '.[] | {iid, title, author: .author.username, state}'
gcloud compute instances list --format=json | jq '.[] | {name, zone, status}'
```

複雜篩選用 jq 的 `select` 串接，保持在同一個 jq 呼叫中：

```bash
kubectl get pods -o json | jq '
  [.items[]
   | select(.status.phase != "Running")
   | select(.metadata.namespace == "production")
   | "\(.metadata.name) \(.status.phase)"]
'
```

> 避免多次 pipe jq（如 `jq '...' | jq '...' | jq '...'`），因為每次都會重新解析整個 JSON。把多個 filter 寫在同一個 jq 表達式裡，用換行保持可讀性即可。

## 操作說明

執行 CLI 指令前，先用中文簡要說明這條指令的用途，讓使用者能理解每一步在做什麼。

## 破壞性操作

CLI 工具經常涉及刪除、合併、關閉、強制推送、修改雲端資源等不可逆操作。執行前先用文字訊息輸出 `⚠️ 破壞性操作：<說明>` 告知使用者，等待確認後才執行。不要用 Bash printf ANSI escape code（Bash tool 不會渲染顏色），直接用 markdown 文字輸出。

## 什麼時候不用 jq

- CLI 工具的預設格式已經夠好讀時（如 `bq query` 的 table 格式、`bq show`、`bq ls`），直接用預設輸出，不需要強制 `--format=json` 再 pipe jq
- 只是查看 metadata、schema、狀態等簡單資訊時，不需要 jq
- 當任務已經超出「解析 JSON 輸出」的範疇——例如需要寫入檔案、呼叫外部 API、做跨來源的 join、或產出圖表——這時候用 Python 或其他工具更合適
- jq 的定位是管道中的 JSON 篩選器，不是通用程式語言。只在需要從 JSON 輸出中篩選、轉換資料時才用。
