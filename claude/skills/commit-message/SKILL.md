---
name: commit-message
description: 根據 staged changes 和過往 commit 歷史產生 commit message
disable-model-invocation: true
allowed-tools: Bash
---

幫使用者產生 commit message。請依照以下步驟：

1. 移動到指定檔案的資料夾
2. 執行 `git status` 查看 staged 和 untracked 檔案。
3. 執行 `git diff --staged` 查看實際變更內容。
4. 執行 `git log --oneline -10` 學習此 repo 的 commit message 風格與慣例。
5. 分析變更內容，撰寫 commit message：
   - 遵循該 repo 過往的 commit message 格式與風格
   - 使用英文撰寫
   - 簡潔扼要（1-2 句）
   - 著重描述「為什麼」而非「做了什麼」
6. 將建議的 commit message 呈現給使用者確認，經同意後再執行 commit。
