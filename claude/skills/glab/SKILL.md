---
name: glab
description: 使用 glab 操作 GitLab 時的規則。任何涉及 glab 的操作都觸發此 skill。搭配 cli skill 處理 JSON 輸出。
user-invocable: true
---

# glab

## 前置步驟

先用 Skill tool 觸發 `/cli` skill，載入 CLI 解析規則（用 jq 不用 Python、破壞性與費用操作確認）。

## 規則：查詢 issue 只用 `glab api`

查詢 issue 一律用 `glab api` 打 REST API v4 或 GraphQL endpoint，**禁止用 `glab issue list` / `glab issue view` 等子命令查詢**。理由：`glab issue view` 會截斷內容、看不到完整資訊；API 回傳完整乾淨的 JSON，可精確篩選。

其餘操作不受限，可正常使用子命令——包括 `glab mr` 建立、`glab issue create` 建立 issue 等。
