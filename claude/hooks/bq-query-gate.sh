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
# 職責邊界：本 hook 只收斂處理「bq 指令有沒有被安全地呼叫」。指令中夾帶的
#           非 bq 危險指令（rm、對外傳輸等）不在此把關——那應由另一支通用
#           危險指令 hook 負責（PreToolUse 可掛多個 hook，任一 deny 即擋）。
#           不在本 hook 用黑名單去認 rm 等，因黑名單注定漏、且會給假安全感。
#
# 判斷規則（針對 Bash 工具的指令字串）：
#   A. 完全不含 bq                → 不表態（走正常權限流程）
#   B. 含「多個 bq 呼叫」          → 全部都是唯讀白名單才放行（不論用 pipe /
#                                    ; / && / 換行 連接，因唯讀無副作用）；
#                                    只要有一個非白名單（query 實跑、dry_run、
#                                    破壞性…）就 deny，要求 ai 拆成獨立指令重送。
#                                    （堵住 dry_run+實跑、show+query 搭便車等）
#                                    註：串接中夾帶的「非 bq」危險指令（rm 等）
#                                        不在此把關，交由通用危險指令 hook。
#   C. 單一 bq：
#       - shell                    → deny（互動模式會卡住）
#       - 唯讀白名單子指令         → 不表態（放行）；接 pipe 處理輸出也放行
#       - query --dry_run          → allow（不掃描、免費）
#       - query（實跑）            → ask（會計費）
#       - 其餘（破壞性 / 未知）    → ask
#
# 輸出格式：PreToolUse 的 hookSpecificOutput.permissionDecision

set -euo pipefail

input="$(cat)"
command="$(printf '%s' "$input" | jq -r '.tool_input.command // ""')"

# --- 決策輸出 helper ---
emit() {  # $1=decision $2=reason
  jq -nc --arg d "$1" --arg reason "$2" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: $d,
      permissionDecisionReason: $reason
    }
  }'
  exit 0
}
ask()   { emit ask   "$1"; }
allow() { emit allow "$1"; }
deny()  { emit deny  "$1"; }

# bq 偵測規則：bq 作為獨立 token（前後為字串邊界或非英數底線 / 空白）
BQ_RE='(^|[^[:alnum:]_])bq([[:space:]]|$)'

# A. 完全不含 bq → 不表態
if ! printf '%s' "$command" | grep -Eq "$BQ_RE"; then
  exit 0
fi

# 指令內 bq 出現次數
bq_count="$(printf '%s' "$command" | grep -oE "$BQ_RE" | wc -l | tr -d '[:space:]')"

# 取第 N 個 bq 的子指令 token（允許 bq 與子指令間插入全域 flag，如 --project_id=foo）。
# 作法：把每個 bq 呼叫片段抓出來，取其後第一個非 - 開頭的 token。
nth_subcmd() {  # $1=index(1-based)
  # (^|[^[:alnum:]_])bq  作為 bq 起點；其後可有全域 flag；再取第一個非 - 開頭 token。
  printf '%s' "$command" \
    | grep -oE '(^|[^[:alnum:]_])bq([[:space:]]+-[^[:space:]]+)*[[:space:]]+[^-[:space:]][^[:space:]]*' \
    | sed -n "${1}p" \
    | grep -oE '[^[:space:]]+$' || true
}

# 唯讀白名單子指令
is_readonly() {  # $1=subcmd
  case "$1" in
    ls|show|head|get-iam-policy|info|version|help|mkdef|wait|cancel) return 0 ;;
    *) return 1 ;;
  esac
}

# --- B. 多個 bq 呼叫：全部都是唯讀白名單才放行（連接方式不限） ---
if [ "$bq_count" != "1" ]; then
  i=1
  while [ "$i" -le "$bq_count" ]; do
    sc="$(nth_subcmd "$i")"
    if ! is_readonly "$sc"; then
      deny "指令含多個 bq 呼叫，其中 bq ${sc:-?} 非唯讀白名單，可能夾帶計費／破壞性操作。請把每條 bq 指令拆成獨立指令分別重送。"
    fi
    i=$((i + 1))
  done
  exit 0
fi

# --- C. 單一 bq ---
subcmd="$(nth_subcmd 1)"

# bq shell：互動模式會卡住 → deny
if [ "$subcmd" = "shell" ]; then
  deny "bq shell 為互動模式會卡住，請由使用者親自執行"
fi

# 唯讀白名單（單一 bq，可接 pipe 處理輸出）→ 放行
if is_readonly "$subcmd"; then
  exit 0
fi

# bq query：dry run 免費放行；實跑計費 → ask
if [ "$subcmd" = "query" ]; then
  if printf '%s' "$command" | grep -Eq -- '--dry[_-]run'; then
    allow "bq query --dry_run 不掃描資料、免費，自動放行"
  fi
  ask "bq query 會實際掃描資料並計費，請確認後再執行"
fi

# 其餘 bq 子指令（cp / extract / insert / load / mk / rm / update / *-iam-policy…
# 及未來未知子指令）→ 破壞性或未知，一律 ask
ask "bq ${subcmd:-操作} 屬破壞性／寫入或未知操作，請確認後再執行"
