---
name: no-unsourced-premises
description: 不要用沒出處的前提一路推演；每個前提附出處，沒出處就停下來問使用者
metadata:
  node_type: memory
  type: feedback
  originSessionId: 40b12731-8e00-4667-ad8a-dbedc91c487a
---

回答時最常見的失誤：為了讓建議聽起來更完整、更有說服力，自行補上沒有出處的前提（例如假想的慣例、前例、分工、技術行為），再以此一路推演出方案。使用者多次當場糾正。

**Why:** 這會連續產出建立在錯誤前提上的方案，浪費雙方時間，也違反「先確認核心事實」。使用者已試過「要我標示事實 vs 推測」，效果差——我仍會把推測標成事實。

**How to apply:**

- 每一個關鍵前提（慣例、前例、分工、某服務的行為）都要能說出「出處在哪」：repo 檔案、issue/MR、Slack thread、官方文件。能查就先查。
- 查不到、或只是我的推測 → **停下來問使用者**，不要先補一個前提再往下推。寧可多問一句。
- 不要為了讓論述更完整/更有說服力，而填入沒有根據的內容。
- 引用來源時編號/類型要精確（例：GitLab issue 編號 ≠ Slack thread），不要混用。

關聯：[[communication-guidelines]]
