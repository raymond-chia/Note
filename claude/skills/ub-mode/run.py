# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""從目標專案目錄執行已安裝的工具，不切換工作目錄。"""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
if len(sys.argv) < 2 or sys.argv[1] not in ("crapper", "dryer", "mutator"):
    raise SystemExit("用法：uv run run.py {crapper|dryer|mutator} [參數]")
manifest = root / "tools/current.json"
if not manifest.exists():
    raise SystemExit("請先執行：uv run install.py")
installation = root / "tools" / json.loads(manifest.read_text())["directory"]
raise SystemExit(subprocess.call([str(installation / ".venv/bin" / sys.argv[1]), *sys.argv[2:]]))
