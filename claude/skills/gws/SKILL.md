---
name: gws
description: 使用 Google Workspace CLI (gws) 讀取 Google Sheets 資料。此 skill 限制為唯讀操作，禁止任何修改、刪除、建立資料的指令。當使用者要查詢 Google Sheets 資料時觸發。搭配 cli skill 使用以處理 JSON 輸出。
user-invocable: true
---

# Google Workspace CLI (gws) — Sheets 唯讀存取

使用 `gws` CLI 查詢 Google Sheets 資料。**本 skill 僅允許唯讀操作。**

載入此 skill 時，同時載入 `cli` skill 以遵循 JSON 輸出的解析規則。

## 前置步驟

執行此 skill 前，先用 Skill tool 觸發 `/cli` skill，確保 CLI 相關規則一併載入。

## 唯讀規則

只允許以下 method：

- `get`、`batchGet`、`batchGetByDataFilter`、`getByDataFilter` — 取得資料
- `+read` — helper 讀取指令
- `schema` — 查看 API schema

**禁止執行以下 method（即使使用者要求也不執行）：**

- `create`、`update`、`batchUpdate`、`batchUpdateByDataFilter`
- `append`、`+append`
- `delete`、`clear`、`batchClear`、`batchClearByDataFilter`
- 任何帶 `--json` body 且目標為寫入用途的請求

遇到寫入請求時，輸出 `⛔ 拒絕：此 skill 僅允許唯讀操作，不執行寫入/修改/刪除指令。` 並停止。

## 常用讀取範例

```bash
# 讀取試算表 metadata（含所有 sheet 名稱與 sheetId）
gws sheets spreadsheets get --params '{"spreadsheetId": "SPREADSHEET_ID"}'

# 讀取特定 range 的值
gws sheets spreadsheets values get --params '{"spreadsheetId": "SPREADSHEET_ID", "range": "Sheet1!A1:Z100"}'

# 批次讀取多個 range
gws sheets spreadsheets values batchGet --params '{"spreadsheetId": "SPREADSHEET_ID", "ranges": ["Sheet1!A:C", "Sheet2!A:B"]}'

# 用 helper 讀取
gws sheets +read --params '{"spreadsheetId": "SPREADSHEET_ID", "range": "Sheet1"}'
```

## 從 URL 解析 Spreadsheet ID

Google Sheets URL 格式：`https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit?gid={SHEET_ID}`

- `/d/` 和 `/edit` 之間的字串 → `spreadsheetId`
- `gid` 參數 → `sheetId`（數字），用 `spreadsheets get` 的 metadata 比對 sheet name 後再組成 range

## 操作說明

執行 gws 指令前，先用中文簡要說明這條指令的用途。
