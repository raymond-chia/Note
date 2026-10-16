# Claude Code Hooks

此目錄的腳本**不會自動載入**。Claude Code 只執行 `settings.json` 中明確註冊的 hook。
放在這裡只是存放點（`~/.claude` symlink 到本 repo，故可用 `~/.claude/hooks/xxx.sh` 引用）。

新增 hook 後，務必在 `~/.claude/settings.json` 的 `hooks` 註冊才會生效，並重開 session。

## 註冊範例

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/bq-query-gate.sh",
            "if": "Bash(bq query:*)"
          }
        ]
      }
    ]
  }
}
```
