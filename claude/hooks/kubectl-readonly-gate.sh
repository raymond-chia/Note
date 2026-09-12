#!/usr/bin/env bash
# PreToolUse hook：只允許唯讀 kubectl 指令，其餘一律擋下
#
# 目的：避免 ai 對 cluster 執行任何非唯讀操作。定位為「防誤觸」，
#       基於指令字串比對，無法對抗刻意繞過（pipe、變數、alias 等）。
#
# 行為：
#   - 非 kubectl 指令            → 不表態（走正常權限流程）
#   - kubectl <唯讀子指令> ...   → 不表態（允許）
#   - 其他 kubectl 子指令        → deny
#
# 判斷：指令需含獨立的唯讀子指令 token（get/logs/describe/top/...），
#       且不得出現任何寫動詞（雙重保險，避免 `get ... && kubectl delete` 之類）。
#       注意：logs -f / --follow 會持續串流卡住，這裡一併擋下。
#       exec 維持在寫動詞黑名單中（即使可作唯讀用途，保守起見不放行）。
#
# 輸出格式：PreToolUse 的 hookSpecificOutput.permissionDecision

set -euo pipefail

command="$(cat | jq -r '.tool_input.command // ""')"

# 非 kubectl → 不表態
printf '%s' "$command" | grep -Eq '(^|[^[:alnum:]_])kubectl([[:space:]]|$)' || exit 0

# 唯讀子指令白名單；同時不得出現任何寫動詞（雙重保險）。
readonly_verbs='get|logs|describe|top|explain|api-resources|api-versions|version|cluster-info|config'
write_verbs='apply|create|delete|edit|patch|replace|scale|rollout|exec|cp|drain|cordon|uncordon|taint|label|annotate|set|attach|port-forward|run|expose|autoscale|kustomize'

# logs 的 follow 模式會卡住串流 → 擋下
if printf '%s' "$command" | grep -Eqw 'logs' \
   && printf '%s' "$command" | grep -Eq '(^|[[:space:]])(-f|--follow)([[:space:]]|=|$)'; then
  jq -nc '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "kubectl logs -f/--follow 會持續串流，請改用 --tail 或由使用者親自執行"
    }
  }'
  exit 0
fi

if printf '%s' "$command" | grep -Eqw "$readonly_verbs" \
   && ! printf '%s' "$command" | grep -Eqw "$write_verbs"; then
  exit 0
fi

jq -nc '{
  hookSpecificOutput: {
    hookEventName: "PreToolUse",
    permissionDecision: "deny",
    permissionDecisionReason: "僅允許 kubectl get；其他 kubectl 指令請由使用者親自執行"
  }
}'
exit 0
