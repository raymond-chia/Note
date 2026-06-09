---
name: bigquery
description: 查詢 BigQuery 資料的通用規則與流程
user-invocable: true
---

# BigQuery 查詢 Skill

協助使用者查詢 BigQuery 資料。核心紀律：**先估再查，能少掃就少掃**——每次掃描都計費，指定日期、用分區過濾、查前先 dry run。

## 前置步驟

執行此 skill 前，先用 Skill tool 觸發 `/cli` skill，載入 CLI 相關規則（含「操作說明」「破壞性操作」）。

## 費用紀律（最重要）

掃描實際資料的 `bq query` 才計費；dry run 與 metadata 讀取（`bq show`、`bq ls`）免費。三道防線缺一不可：

1. **每次實際查詢前都先 dry run、報掃描量、等使用者確認，無一例外。**
   重跑、改輸出格式（`--format`）、加 `--nouse_cache`、為除錯而再查、調整 jq 後重抓——全都算一次新的實際查詢，一律重走「dry run → 告知 → 等確認」。
   結果看起來不對、想「再跑一次看看」時**最容易違規**：dry run 幾乎免費、實際查詢才計費，先重跑實際查詢是把順序做反。要除錯，先改 SQL 再 dry run，不要靠重複實際掃描來試。
2. **實際執行固定加 `--maximum_bytes_billed=17179869184`**（16 GiB，約 $0.1）當硬防線：超過上限直接失敗、不計費。
   **用固定值，不要依預估動態調整**，否則等於自己放行、防線形同虛設。確實要掃更大範圍時，才在當次明確調高並告知使用者。
3. **指定日期 + 分區過濾**（這才是降掃描量、降費用的關鍵）：
   - 未提供日期時，**必先詢問**，不可省略。
   - 日期年份以 system-reminder 的 `currentDate` 為準；使用者只說「M/D」時，年份取 `currentDate` 的年份，不可自行假設。
   - 用分區欄位（`_PARTITIONDATE` / `_PARTITIONTIME` 或自訂分區欄位）過濾日期範圍。

## 執行流程

1. 確認使用者已提供日期（否則先問）。
2. **若尚未確認 table schema**（沒讀過本地 schema 檔、或首次查該 table），先讀（免費）：
   ```
   bq show --format=json <project>:<dataset>.<table> | jq '{schema, timePartitioning, rangePartitioning, clustering}'
   ```
3. 組合 SQL：含日期/分區過濾與 `LIMIT`，用 Standard SQL（`--use_legacy_sql=false`）。
4. Dry run 估掃描量：
   ```
   bq query --use_legacy_sql=false --dry_run 'SQL'
   ```
5. 告知使用者預估掃描量，**等確認**。
6. 實際執行（帶費用保險絲）：
   ```
   bq query --use_legacy_sql=false --maximum_bytes_billed=17179869184 'SQL'
   ```
   輸出格式：給人看用預設 table；需程式處理才加 `--format=json`。
7. 整理結果呈現給使用者。

## 陷阱

### 查詢輸出控制（與費用無關）

`LIMIT` 與 `--max_rows` 都只控制輸出列數，**不影響掃描量、不降費用**（BigQuery 先掃完整個過濾範圍才套 `LIMIT`）。降費用靠分區過濾，見上方費用紀律。

- SQL 加 `LIMIT` 避免意外把大量資料灌進終端機。
- `bq query` 預設只回 **前 100 列**（CLI 端 `--max_rows` 預設值），與 SQL 的 `LIMIT` 無關。即使 `LIMIT 500`、實際也有 500 種組合，輸出仍只有 100 列，長尾被靜默丟掉。
- **做 `GROUP BY`、或預期結果可能超過 100 列時，務必加 `--max_rows=<夠大的值>`**（如 `--max_rows=100000`）。`--max_rows` 只影響回傳列數、不影響掃描量（不增費、dry run 數字不變）。
- 驗證是否被截斷：各列計數加總 vs 直接 `COUNT(*)`，對不上就是被截斷。

### Metadata 探索的誤判

- `bq ls` 預設只列 **50** 筆 tables，排序未定義（通常接近建立時間）。**別因只看到舊 table 就判斷 dataset 沒新資料。** 要確認是否仍有新資料，用足夠大的 `--max_results` 排序取末幾筆：
  ```
  bq ls --max_results=10000 --format=json project:dataset | jq '[.[].tableReference.tableId] | sort | .[-10:]'
  ```
- `bq show` 的 `lastModifiedTime` 是 metadata（ACL、description 等）修改時間，**不代表最後資料寫入時間**，不可用來判斷 dataset 是否仍在使用中。

## 常見錯誤處理

- **其他錯誤**：將完整錯誤訊息呈現給使用者，不要自行猜測原因。
