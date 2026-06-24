#!/usr/bin/env bash
# PreToolUse hook：bq query 費用閘門
#
# 目的：實際掃描資料的 `bq query` 會計費，必須由使用者親自確認；
#       免費的 dry run 與 metadata 操作則自動放行。
#       skill 無法真正阻止 ai 擅自呼叫 bq query。
#
# 行為（針對 Bash 工具的指令字串）：
#   - 含 `bq query` 且含 `--dry_run` / `--dry-run` → allow（自動執行，不問）
#   - 含 `bq query` 但不含 dry run 旗標          → ask（跳出確認框，使用者親自按）
#   - 其他指令                                   → 不表態，交回正常權限流程
#
# 輸出格式：PreToolUse 的 hookSpecificOutput.permissionDecision

set -euo pipefail

input="$(cat)"

command="$(printf '%s' "$input" | jq -r '.tool_input.command // ""')"

# 不是 bq query 就不表態（exit 0、無輸出 → 走正常權限流程）
if ! printf '%s' "$command" | grep -Eq '(^|[^[:alnum:]_])bq[[:space:]]+query([[:space:]]|$)'; then
  exit 0
fi

# 含 dry run 旗標 → 放行
if printf '%s' "$command" | grep -Eq -- '--dry[_-]run'; then
  jq -nc '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "allow",
      permissionDecisionReason: "bq query --dry_run 不掃描資料、免費，自動放行"
    }
  }'
  exit 0
fi

# 其餘 bq query → 要求使用者確認
jq -nc '{
  hookSpecificOutput: {
    hookEventName: "PreToolUse",
    permissionDecision: "ask",
    permissionDecisionReason: "bq query 會實際掃描資料並計費，請確認後再執行"
  }
}'
exit 0
