"""共用的 MIDI→WAV 產生方法。

整個 music/ 底下「產生 wav」只有這一份實作：
    任何來源 --> 一個 .mid --midi_to_wav()--> 一個 .wav

- music21：Stream.write('midi') 產出 .mid，再交給 midi_to_wav()
- alda   ：alda export 產出 .mid，再交給 midi_to_wav()（介面預留，見 alda_to_midi）

合成引擎統一用 timidity（自帶音色，零額外設定）。
"""

import subprocess
from pathlib import Path

# 輸出結構：midi 與 wav 分資料夾
MIDI_DIR = Path(__file__).parent / "output" / "midi"
WAV_DIR = Path(__file__).parent / "output" / "wav"


def midi_to_wav(midi_path: Path, wav_path: Path) -> Path:
    """唯一一份 MIDI→WAV 實作：用 timidity 把 .mid 合成成 .wav。

    對應舊 alda Makefile 的：timidity <mid> -Ow -o <wav>
    -Ow = 輸出 RIFF WAVE 檔。
    """
    wav_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["timidity", str(midi_path), "-Ow", "-o", str(wav_path)],
        check=True,
        capture_output=True,
    )
    return wav_path


def play(wav_path: Path) -> None:
    """用 macOS 的 afplay 試聽。"""
    subprocess.run(["afplay", str(wav_path)], check=True)


def alda_to_midi(alda_path: Path, midi_path: Path) -> Path:
    """（介面預留）用 alda export 把 .alda 產出 .mid，之後再接 midi_to_wav()。

    目前機器上沒有 alda 執行檔，故僅保留介面、尚未啟用。
    之後決定要不要走 alda 這條路時，再實作：
        alda export -f <alda> -o <midi> -O midi
    """
    raise NotImplementedError("alda 這條路尚未啟用（機器上目前沒有 alda）")
