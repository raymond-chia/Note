---
name: notion
description: 讀取 Notion 內容、在本地編輯、再寫回 Notion 時的注意事項。重點：Notion 的 link 無法可靠地被複製／還原，寫回時必須保留原始 link 不動。當任務涉及抓 Notion 頁面下來改、或把改好的內容寫回 Notion 時觸發。
user-invocable: true
---

# notion

## 核心問題

Notion 的 link 無法可靠地被複製、也無法用純文字重建。透過 `notion-fetch` 抓下來的 Markdown 中，link 常呈現為：

- Notion 內部相對路徑 + 區塊 hash，例如 `/368ae1da87ee8047862cd28775da1d11?pvs=25#369ae1da87ee802fa421c627e23e0d4e`
- 帶 `?pvs=21` / `?pvs=25` 等 query 的頁面連結
- `discussion://...` 這類非 URL 的內部引用

這些字串一旦被當成一般文字改動、格式化、或「順手清理」，寫回 Notion 後 link 就會失效或指向錯誤區塊，且**無法從文字回推正確目標**。

## 規則

1. **link 一律視為不可變 token**：編輯時不碰 link 的 URL 部分（`(...)` 內、`discussion://`、含 hash / `?pvs=` 的字串）。只在必要時改 link 的顯示文字（`[顯示文字]` 內），且要明確知道自己在改顯示文字。

2. **不重排、不正規化 link**：不要「整理」query string、不要補全相對路徑成絕對 URL、不要移除看似多餘的 hash、不要統一格式。看似冗餘的部分往往是 Notion 定位區塊的關鍵。

3. **改動前先定位、精準替換**：用 Edit 做最小範圍的字串替換，`old_string` 不要涵蓋到 link；能不把 link 放進 `old_string`／`new_string` 就不要放。若非得包含，`new_string` 要一字不差地保留原 link。

4. **寫回前 diff 檢查 link**：寫回 Notion 前，先比對編輯前後所有 link，確認 URL 部分完全沒變（連 `?pvs=21` vs `?pvs=25` 的差異都算變動）。有任何 link 被動到就停下來，先跟使用者確認。

5. **寫回 Notion 為對外／可能破壞性操作**：依協作偏好，寫回 Notion 前先確認；不確定 link 是否被影響時，寧可先出草稿或先問，不要直接覆蓋。
