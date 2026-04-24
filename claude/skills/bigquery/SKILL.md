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

- 遵循 `cli` skill 的「操作說明」和「破壞性操作」規則
- 若使用者未提供日期，**必須先詢問日期再執行查詢**，不可省略。
- 使用 Standard SQL（`--use_legacy_sql=false`）
- 輸出格式依用途選擇：查詢結果直接給人看時用預設 table 格式即可，需要程式處理時才用 `--format=json`
- 查詢前先用 `--dry_run` 確認掃描量，告知使用者後再執行
- SQL 中應加上 `LIMIT` 避免意外大量輸出

## 執行流程

1. 確認使用者提供了日期
2. 組合 SQL，確保包含日期過濾與 `LIMIT`
3. `bq query --use_legacy_sql=false --dry_run 'SQL'` 確認掃描量
4. 告知使用者預估掃描量，確認後執行實際查詢
5. `bq query --use_legacy_sql=false 'SQL'`
6. 整理結果呈現給使用者

## 日期過濾

使用分區欄位（`_PARTITIONDATE` / `_PARTITIONTIME` 或自訂分區欄位）過濾日期範圍。

## 注意事項

- `bq ls` 預設只列出 **50** 筆 tables，排序順序未定義（通常接近建立時間）。**不要因為只看到舊 table 就判斷 dataset 沒有新資料寫入。**
- 要確認 dataset 是否仍有新資料，應使用足夠大的 `--max_results` 並排序取最後幾筆，例如：`bq ls --max_results=10000 --format=json project:dataset | jq '[.[].tableReference.tableId] | sort | .[-10:]'`
- `bq show` 的 `lastModifiedTime` 是 dataset metadata 的修改時間（如 ACL、description 變更），**不代表最後一次資料寫入時間**，不可用來判斷 dataset 是否仍在使用中

## 常見錯誤處理

- **其他錯誤**：將完整錯誤訊息呈現給使用者，不要自行猜測原因
