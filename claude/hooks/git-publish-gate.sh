#!/usr/bin/env bash
# PreToolUse hook：git push / 建立 MR / 建立 issue 人工同意閘門
#
# 目的：對外發布性的操作（推送到遠端、開 MR、開 issue）影響範圍大、
#       不易撤銷，必須由使用者親自確認；ai 不應擅自執行。
#       skill / 規範無法真正阻止 ai 直接呼叫這些指令，故用 hook 強制 ask。
#
# 行為（針對 Bash 工具的指令字串）：
#   - 含 `git push`                         → ask（跳出確認框，使用者親自按）
#   - 含 `glab mr create` / `gh pr create`  → ask
#   - 含 `glab issue create` / `gh issue create` → ask
#   - 其他指令                              → 不表態，交回正常權限流程
#
# 輸出格式：PreToolUse 的 hookSpecificOutput.permissionDecision

set -euo pipefail

input="$(cat)"

command="$(printf '%s' "$input" | jq -r '.tool_input.command // ""')"

# git push
if printf '%s' "$command" | grep -Eq '(^|[^[:alnum:]_])git[[:space:]]+(.+[[:space:]])?push([[:space:]]|$)'; then
  jq -nc '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "ask",
      permissionDecisionReason: "git push 會推送到遠端，請確認後再執行"
    }
  }'
  exit 0
fi

# 建立 MR / PR
if printf '%s' "$command" | grep -Eq '(^|[^[:alnum:]_])(glab[[:space:]]+mr|gh[[:space:]]+pr)[[:space:]]+create([[:space:]]|$)'; then
  jq -nc '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "ask",
      permissionDecisionReason: "建立 MR/PR 為對外發布操作，請確認後再執行"
    }
  }'
  exit 0
fi

# 建立 issue
if printf '%s' "$command" | grep -Eq '(^|[^[:alnum:]_])(glab|gh)[[:space:]]+issue[[:space:]]+create([[:space:]]|$)'; then
  jq -nc '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "ask",
      permissionDecisionReason: "建立 issue 為對外發布操作，請確認後再執行"
    }
  }'
  exit 0
fi

# glab/gh api 的寫入呼叫
#   破口：貼 note、改狀態、close、merge 等對外寫入多半走 `glab api --method POST ...`，
#         既不是 create 子命令也不是 push，會被前面規則漏掉。
#   判準：偵測寫入動作而非單純「有沒有 method」——
#     1. method 為寫入型動詞 (POST/PUT/PATCH/DELETE)，或
#     2. 未寫 method 但帶了 --field/-f/--raw-field/-F/--form
#        (glab 說明明載這些旗標會把預設 GET 轉成 POST，指令字串裡看不到 method)
#   放行：讀取 (預設 GET，含顯式 --method GET)。
#   註：--input 不納入隱式判定——其本身不保證轉 POST，且與 --field 並用時
#       會把 field 當成 URL query；實務上搭 --input 寫入幾乎都會明寫 --method POST，
#       由規則 1 攔到。
#   出處：glab api --help
if printf '%s' "$command" | grep -Eq '(^|[^[:alnum:]_])(glab|gh)[[:space:]]+api([[:space:]]|$)'; then
  if printf '%s' "$command" | grep -Eiq -- '--method[[:space:]=]+(POST|PUT|PATCH|DELETE)|(^|[[:space:]])-X[[:space:]]*(POST|PUT|PATCH|DELETE)'; then
    is_write=1
  elif printf '%s' "$command" | grep -Eq -- '--method[[:space:]=]|(^|[[:space:]])-X([[:space:]]|=)'; then
    # 有顯式 method 但非寫入型 (GET/HEAD/OPTIONS) → 放行
    is_write=0
  elif printf '%s' "$command" | grep -Eq -- '(^|[[:space:]])(--field|--raw-field|--form|-f|-F)([[:space:]]|=)'; then
    # 無顯式 method，但帶了會觸發隱式 POST 的旗標 (依 glab api --help)
    is_write=1
  else
    is_write=0
  fi

  if [ "$is_write" = 1 ]; then
    jq -nc '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "ask",
        permissionDecisionReason: "glab/gh api 寫入操作（貼 note／改狀態／merge／close 等）為對外發布，請確認後再執行"
      }
    }'
    exit 0
  fi
fi

# 其他指令不表態（exit 0、無輸出 → 走正常權限流程）
exit 0
