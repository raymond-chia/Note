"""把 music21 的 Stream 輸出成 MIDI 和 WAV，並試聽。

整條鏈：music21 Stream --.write('midi')--> .mid --midi_to_wav()--> .wav --afplay--> 喇叭

「產生 wav」的實作不在這裡，統一放在 midi_utils.midi_to_wav（timidity）。
"""

from music21 import stream

import midi_utils


def render(score: stream.Stream, name: str, play: bool = True):
    """把 score 存成 output/midi/<name>.mid 和 output/wav/<name>.wav，回傳 wav 路徑。"""
    midi_path = midi_utils.MIDI_DIR / f"{name}.mid"
    wav_path = midi_utils.WAV_DIR / f"{name}.wav"

    # 1) music21 直接寫 MIDI
    midi_path.parent.mkdir(parents=True, exist_ok=True)
    score.write("midi", fp=str(midi_path))

    # 2) MIDI→WAV（共用實作，timidity）
    midi_utils.midi_to_wav(midi_path, wav_path)

    # 3) 試聽
    if play:
        midi_utils.play(wav_path)

    print(f"✓ {midi_path.name}  +  {wav_path.name}")
    return wav_path
