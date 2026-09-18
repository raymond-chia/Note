---
name: bigquery-schema-change-avoid-rebuild
description: 改 BigQuery table schema 時，哪些操作免重建、哪些會被迫整表重建
metadata:
  type: reference
---

改 BigQuery table schema 時，優先選「不需要重建整張表」的做法。

**Why:** 重建整表要全表掃描＋重灌資料，成本高、有中斷風險。BigQuery 官方文件（[修改資料表結構定義](https://cloud.google.com/bigquery/docs/managing-table-schemas)，2026-07-12 更新）明確列出哪些可原地改、哪些不行。

**How to apply:**

免重建（原地 DDL / metadata 操作，DDL 陳述式本身不計費）：
- 加欄位（一律加在最後面，NULLABLE 或 REPEATED）
- `ALTER TABLE ... RENAME COLUMN`
- `ALTER COLUMN SET DATA TYPE`（限官方支援的轉換清單，如 INT64 → NUMERIC）
- REQUIRED 放寬成 NULLABLE
- 改 default value / description
- `ALTER TABLE ... DROP COLUMN`（不立即釋放儲存空間）

必須重建整表：
- **在 schema 中間插入欄位** — 官方原文：「您無法在資料表結構定義中間新增資料欄。系統一律會在資料表或欄位的結尾新增資料欄和巢狀欄位。」唯一做法是建新表再把資料複製過去。所以**不要為了欄位順序好看而插中間**，一律往後加。
- NULLABLE → REQUIRED、REPEATED → NULLABLE
- 不在支援清單內的型別轉換（要 `CAST` + 覆寫，全表掃描）
- 複雜巢狀變更（例如改 ARRAY<STRUCT> 內欄位型別），要 `CREATE OR REPLACE TABLE ... AS SELECT`
- 想立刻回收 DROP COLUMN 的儲存空間

相關：[[official-docs-use-browser]]
