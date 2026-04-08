---
name: bigquery
description: 查詢 BigQuery 資料的通用規則與流程
user-invocable: true
---

# BigQuery 查詢 Skill

協助使用者查詢 BigQuery 資料。為了減少掃描的資料量與費用，**必須指定查詢日期**。

## 前置步驟

執行此 skill 前，先用 Skill tool 觸發 `/cli` skill，確保 CLI 相關規則一併載入。

## 規則

- **每個操作前先用中文說明**即將執行的指令與目的，讓使用者能理解每一步在做什麼
- **若指令具破壞性（DELETE、DROP、TRUNCATE、UPDATE 等寫入操作），必須先以文字訊息輸出 `⚠️ 破壞性操作：<說明>` 告知使用者，並等待確認後才執行**（注意：不要用 Bash printf ANSI escape code，因為 Bash tool 不會渲染顏色，直接用 markdown 文字輸出即可）
- 若使用者未提供日期，**必須先詢問日期再執行查詢**，不可省略。
- 使用 Standard SQL（`--use_legacy_sql=false`）
- 輸出格式依用途選擇：查詢結果直接給人看時用預設 table 格式即可，需要程式處理時才用 `--format=json`
- 查詢前先用 `--dry_run` 確認掃描量，告知使用者後再執行
- SQL 中應加上 `LIMIT` 避免意外大量輸出

## 日期過濾

使用分區欄位（`_PARTITIONDATE` / `_PARTITIONTIME` 或自訂分區欄位）過濾日期範圍。

## 執行流程

1. 確認使用者提供了日期
2. 組合 SQL，確保包含日期過濾與 `LIMIT`
3. `bq query --use_legacy_sql=false --dry_run 'SQL'` 確認掃描量
4. 告知使用者預估掃描量，確認後執行實際查詢
5. `bq query --use_legacy_sql=false 'SQL'`
6. 整理結果呈現給使用者

## 常見錯誤處理

- **其他錯誤**：將完整錯誤訊息呈現給使用者，不要自行猜測原因
