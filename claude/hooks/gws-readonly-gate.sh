#!/usr/bin/env bash
# PreToolUse hook：只允許唯讀 gws (Google Workspace CLI) 指令，其餘一律擋下
#
# 目的：避免 ai 對 Google Workspace（Sheets / Docs / Drive 等）執行任何
#       寫入、修改、刪除操作。定位為「防誤觸」，基於指令字串比對，
#       無法對抗刻意繞過（pipe、變數、alias 等）。
#
# 行為：
#   - 非 gws 指令              → 不表態（走正常權限流程）
#   - gws <唯讀 method> ...    → 不表態（允許）
#   - 其他 gws method          → deny
#
# 判斷：gws 的 method 在指令中是獨立 token（gws <service> <resource> <method>）。
#       指令需含獨立的唯讀 method token（get/batchGet/schema/+read/...），
#       且不得出現任何寫 method（雙重保險，避免 `get ... && gws ... batchUpdate`）。
#
# 輸出格式：PreToolUse 的 hookSpecificOutput.permissionDecision
#
# 註：method 名稱含 `+`（如 +read），grep -w 的 word boundary 不認 `+`，
#     故唯讀比對用顯式邊界 (^|[[:space:]]) 而非 -w。

set -euo pipefail

command="$(cat | jq -r '.tool_input.command // ""')"

# 非 gws → 不表態
printf '%s' "$command" | grep -Eq '(^|[^[:alnum:]_])gws([[:space:]]|$)' || exit 0

# 唯讀 method 白名單（含 helper +read）
readonly_methods='get|batchGet|batchGetByDataFilter|getByDataFilter|schema|\+read'

# 寫入 method 黑名單（雙重保險）
write_methods='create|update|batchUpdate|batchUpdateByDataFilter|append|\+append|delete|clear|batchClear|batchClearByDataFilter|copyTo|duplicate|move|trash'

deny() {
  jq -nc --arg reason "$1" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: $reason
    }
  }'
  exit 0
}

# 出現任何寫 method → 直接擋
if printf '%s' "$command" | grep -Eq "(^|[[:space:]])($write_methods)([[:space:]]|=|$)"; then
  deny "gws 僅允許唯讀操作；偵測到寫入/修改/刪除 method，請由使用者親自執行"
fi

# 命中唯讀白名單 → 放行
if printf '%s' "$command" | grep -Eq "(^|[[:space:]])($readonly_methods)([[:space:]]|=|$)"; then
  exit 0
fi

# 既非已知唯讀也非已知寫入 → 保守擋下
deny "gws 指令未命中唯讀 method 白名單；僅允許 get/batchGet/schema/+read 等唯讀操作"
