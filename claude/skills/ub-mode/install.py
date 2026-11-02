# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""下載最新工具並透過 uv 建立本機環境（macOS／Linux）。"""
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent
TOOLS = ROOT / "tools"
NAMES = ("crapper", "dryer", "mutator")


def main():
    if sys.platform not in ("darwin", "linux"):
        raise SystemExit("僅支援 macOS／Linux。")
    uv = shutil.which("uv")
    if not uv:
        raise SystemExit("請先安裝 uv。")
    TOOLS.mkdir(exist_ok=True)
    # 每次使用獨立目錄；失敗時保留原先可用環境。
    installation = Path(tempfile.mkdtemp(prefix="install-", dir=TOOLS))
    versions = {}
    try:
        for name in NAMES:
            url = f"https://codeload.github.com/unclebob/{name}/zip/HEAD"
            with urllib.request.urlopen(url, timeout=60) as response:
                archive = response.read()
            with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
                sha = bundle.comment.decode("ascii").strip() or "HEAD"
            versions[name] = sha
            destination = installation / name
            destination.mkdir()
            with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
                for member in bundle.infolist():
                    relative = Path(*Path(member.filename).parts[1:])
                    target = destination / relative
                    if not target.resolve().is_relative_to(destination.resolve()):
                        raise ValueError("壓縮檔包含不安全路徑")
                    if member.is_dir():
                        target.mkdir(parents=True, exist_ok=True)
                    else:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_bytes(bundle.read(member))
            print(f"已下載 {name}: {sha}", flush=True)
        venv = installation / ".venv"
        subprocess.run([uv, "venv", str(venv)], check=True)
        command = [uv, "pip", "install", "--python", str(venv / "bin/python")]
        for name in NAMES:
            command.extend(["-e", str(installation / name)])
        subprocess.run(command, check=True)
        for name in NAMES:
            subprocess.run([str(venv / "bin" / name), "--help"], check=True, stdout=subprocess.DEVNULL)
        manifest = TOOLS / "current.json"
        temporary = TOOLS / "current.json.tmp"
        temporary.write_text(json.dumps({"directory": installation.name, "commits": versions}, indent=2) + "\n")
        temporary.replace(manifest)
    except BaseException:
        shutil.rmtree(installation)
        raise
    # 新環境已生效，移除舊環境。
    for old in TOOLS.glob("install-*"):
        if old != installation:
            shutil.rmtree(old)
    print("安裝完成。")


if __name__ == "__main__":
    main()
