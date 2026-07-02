#!/usr/bin/env bash
# PreToolUse hook：bq 操作閘門（計費查詢 + 破壞性操作）
#
# 目的：對 BigQuery 的兩類操作要求使用者親自確認，ai 不應擅自執行；
#       skill / 規範無法真正阻止 ai 直接呼叫 bq，故用 hook 強制把關。
#         1. 計費：實際掃描資料的 `bq query` 會產生費用。
#         2. 破壞性 / 寫入：改資料、改結構、改權限、對外匯出等。
#       採白名單策略（比照 kubectl / gws gate）：只放行已知唯讀子指令，
#       其餘（含未來 bq 新增的子指令）一律 ask，安全優先、不漏擋。
#
# 行為（針對 Bash 工具的指令字串）：
#   - 非 bq 指令                         → 不表態（走正常權限流程）
#   - bq query --dry_run                 → allow（不掃描資料、免費，自動放行）
#   - bq shell                           → deny（互動模式會卡住，ai 不該用）
#   - bq <唯讀白名單子指令>              → 不表態（放行）
#   - 其餘 bq 子指令（query / 破壞性 / 未知）→ ask（使用者親自確認）
#
# 輸出格式：PreToolUse 的 hookSpecificOutput.permissionDecision

set -euo pipefail

input="$(cat)"

command="$(printf '%s' "$input" | jq -r '.tool_input.command // ""')"

# 不是 bq 指令就不表態（exit 0、無輸出 → 走正常權限流程）
if ! printf '%s' "$command" | grep -Eq '(^|[^[:alnum:]_])bq([[:space:]]|$)'; then
  exit 0
fi

# 取出 bq 後面第一個「子指令」token：
#   允許 bq 與子指令之間插入全域 flag（-foo / --foo=bar / --location US 的分離值），
#   例如 `bq --project_id=foo query`、`bq --location US show`。
#   作法：抓 bq 之後、第一個不以 - 開頭的 token 視為子指令。
#   代價：理論上 `--location US` 的值 US 會被當成子指令，但 bq 全域 flag 的值
#         不會與子指令名稱（query/show/...）相同，落入白名單之外時頂多多問一次，
#         安全優先可接受。
subcmd="$(printf '%s' "$command" \
  | grep -oE '(^|[^[:alnum:]_])bq([[:space:]]+-[^[:space:]]+)*[[:space:]]+[^-[:space:]][^[:space:]]*' \
  | head -1 \
  | grep -oE '[^[:space:]]+$' || true)"

ask() {
  jq -nc --arg reason "$1" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "ask",
      permissionDecisionReason: $reason
    }
  }'
  exit 0
}

allow() {
  jq -nc --arg reason "$1" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "allow",
      permissionDecisionReason: $reason
    }
  }'
  exit 0
}

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

# 唯讀白名單（出處：bq help 子指令清單）。
# get-iam-policy 唯讀；set/add/remove-iam-policy 改權限 → 不在白名單，落入 ask。
case "$subcmd" in
  ls|show|head|get-iam-policy|info|version|help|mkdef|wait|cancel)
    # query --dry_run 例外處理在下方；這裡是純唯讀子指令，放行不表態
    exit 0
    ;;
esac

# bq shell：互動模式會卡住串流，且 ai 不該進互動 → 直接 deny
if [ "$subcmd" = "shell" ]; then
  deny "bq shell 為互動模式會卡住，請由使用者親自執行"
fi

# bq query：dry run 免費放行；其餘計費 → ask
if [ "$subcmd" = "query" ]; then
  if printf '%s' "$command" | grep -Eq -- '--dry[_-]run'; then
    allow "bq query --dry_run 不掃描資料、免費，自動放行"
  fi
  ask "bq query 會實際掃描資料並計費，請確認後再執行"
fi

# 其餘所有 bq 子指令（cp / extract / insert / load / mk / partition / rm /
# truncate / undelete / update / *-iam-policy / init，以及未來新增的未知子指令）
# → 破壞性或未知，一律 ask
ask "bq ${subcmd:-操作} 屬破壞性／寫入或未知操作，請確認後再執行"
