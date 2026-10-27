"""MIDI→WAV 合成。

兩顆音源：Salamander Grand Piano（Yamaha C5 取樣，音色較好但只有鋼琴）、
FluidR3_GM（128 個樂器齊全）。

MUSIC_SOUNDFONT 可指定任一顆蓋過搜尋結果。
MUSIC_SOUNDFONT=xxx uv run xxx.py

安裝：
    sudo apt install -y fluidsynth fluid-soundfont-gm    # Debian/Ubuntu
    brew install fluid-synth                             # macOS，音源需另外下載
Salamander：freepats.zenvoid.org/Piano/（CC-BY 3.0, Alexander Holm），soundfonts/ 不進 git。
"""

import os
import subprocess
import sys
from pathlib import Path

# 輸出結構：midi 與 wav 分資料夾
MIDI_DIR = Path(__file__).parent / "output" / "midi"
WAV_DIR = Path(__file__).parent / "output" / "wav"

# 只認這兩台：Linux（apt 的 fluid-soundfont-gm）與 mac（Homebrew 的 fluid-synth）
SOUNDFONT_DIRS = [
    Path(__file__).parent / "soundfonts",   # 專案自帶（不進 git）
    Path("/usr/share/sounds/sf2"),          # Linux
    Path("/opt/homebrew/share/fluidsynth"), # macOS
]
DEFAULT_SOUNDFONT = "FluidR3_GM.sf2"
PIANO_SOUNDFONT = "SalamanderGrandPiano.sf2"   # Yamaha C5 取樣，只有鋼琴


def find_soundfont(piano_only: bool = False) -> Path:
    """找音源。MUSIC_SOUNDFONT 有設就用它（相對路徑以本檔目錄為基準）。

    piano_only=True 優先挑 PIANO_SOUNDFONT，沒有這顆時退回 DEFAULT_SOUNDFONT。
    """
    env = os.environ.get("MUSIC_SOUNDFONT")
    if env:
        path = Path(env).expanduser()
        if not path.is_absolute():
            path = Path(__file__).parent / path
        if not path.is_file():
            raise FileNotFoundError(f"MUSIC_SOUNDFONT 指定的音源不存在：{path}")
        return path

    if piano_only:
        for directory in SOUNDFONT_DIRS:
            candidate = directory / PIANO_SOUNDFONT
            if candidate.is_file():
                return candidate

    for directory in SOUNDFONT_DIRS:
        candidate = directory / DEFAULT_SOUNDFONT
        if candidate.is_file():
            return candidate

    searched = "\n".join(f"  {d}" for d in SOUNDFONT_DIRS)
    raise FileNotFoundError(
        f"找不到 {DEFAULT_SOUNDFONT}。搜尋過的目錄：\n{searched}\n"
        "可用 MUSIC_SOUNDFONT=<path> 指定。"
    )


def midi_to_wav(midi_path: Path, wav_path: Path, piano_only: bool = False) -> Path:
    wav_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["fluidsynth", "-ni", "-r", "44100", "-F", str(wav_path),
         str(find_soundfont(piano_only)), str(midi_path)],
        check=True,
        capture_output=True,
    )
    return wav_path


def play(wav_path: Path) -> None:
    """試聽：mac 用 afplay，Linux 用 aplay。"""
    cmd = ["afplay"] if sys.platform == "darwin" else ["aplay", "-q"]
    subprocess.run([*cmd, str(wav_path)], check=True)


def alda_to_midi(alda_path: Path, midi_path: Path) -> Path:
    """（介面預留）用 alda export 把 .alda 產出 .mid，之後再接 midi_to_wav()。

    目前機器上沒有 alda 執行檔，故僅保留介面、尚未啟用。
    之後決定要不要走 alda 這條路時，再實作：
        alda export -f <alda> -o <midi> -O midi
    """
    raise NotImplementedError("alda 這條路尚未啟用（機器上目前沒有 alda）")
