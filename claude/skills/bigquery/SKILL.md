---
name: bigquery
description: 查詢 BigQuery 資料的通用規則與流程
user-invocable: true
allowed-tools: Bash
---

# BigQuery 查詢 Skill

協助使用者查詢 BigQuery 資料。為了減少掃描的資料量與費用，**必須指定查詢日期**。

## 規則

- 若使用者未提供日期，**必須先詢問日期再執行查詢**，不可省略。
- 使用 Standard SQL（`--use_legacy_sql=false`）
- 查詢前先用 `--dry_run` 確認掃描量，告知使用者後再執行
- SQL 中應加上 `LIMIT` 避免意外大量輸出

## 日期過濾

使用分區欄位（`_PARTITIONDATE` / `_PARTITIONTIME` 或自訂分區欄位）過濾日期範圍。

## 執行流程

1. 確認使用者提供了日期
2. 組合 SQL，確保包含日期過濾與 `LIMIT`
3. `bq query --use_legacy_sql=false --dry_run 'SQL'` 確認掃描量
4. 告知使用者預估掃描量，確認後執行實際查詢
5. 整理結果呈現給使用者
