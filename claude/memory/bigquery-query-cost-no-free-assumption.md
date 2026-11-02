---
name: bigquery-query-cost-no-free-assumption
description: 估 BigQuery 查詢費用時，不可預設有免費額度，也不可當作掃 0 筆就免費
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 08436453-d8c7-445f-8e8d-b5a459f399b3
  modified: 2026-09-18T05:09:34.064Z
---

估 BigQuery 查詢費用時，直接給絕對金額，不要扣免費額度。

**Why:** 每月前 1 TiB 免費是「per month / **account**」，整個 billing account 共用，不是每個 project 一份，多半早被其他 project 吃掉。另外查詢有 **10 MB 最低計費**（每個參照的 table、每次查詢各自適用），掃空 partition 也算錢。兩者都查自[官方定價](https://cloud.google.com/bigquery/pricing)。

**How to apply:** 算 bytes 時套 10 MB 下限，乘 US$6.25/TiB 給金額。小到無所謂就說「一個月不到 1 美分」，別搬免費額度當理由。

相關：[[official-docs-use-browser]]、[[bigquery-schema-change-avoid-rebuild]]
