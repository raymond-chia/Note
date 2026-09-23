---
name: official-docs-use-browser
description: 需要查官方文件／牌價時，優先用瀏覽器抓頁面，不要先試 WebFetch/WebSearch
metadata:
  node_type: memory
  type: feedback
  originSessionId: 2a7ff612-f595-479e-b1ac-dd26b8d5afef
  modified: 2026-07-24T01:04:40.319Z
---

需要查官方文件（官方牌價、官方 API 文件等）時，直接用瀏覽器抓頁面：`preview_start` 開頁 → `get_page_text` 取內容。不要先用 WebFetch 或 WebSearch。

**Why:** WebFetch 抓 GCP 官方頁面常被截斷（例如 BigQuery pricing 抓到的是空殼）。瀏覽器的 `get_page_text` 能完整取得動態渲染後的內容。

**How to apply:** 一判斷出要查官方文件，第一手就開瀏覽器，省掉 WebFetch 被截斷後再轉換的來回。
