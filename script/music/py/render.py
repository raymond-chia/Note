"""把 music21 的 Stream 輸出成 MIDI 和 WAV，並試聽。

整條鏈：music21 Stream --.write('midi')--> .mid --midi_utils.midi_to_wav()--> .wav
音源由樂器編制決定：全鋼琴用 Salamander（Yamaha C5 取樣，音色較好），
有其他樂器時它涵蓋不到，改用 FluidR3_GM。
"""

from music21 import instrument, stream

import midi_utils


def _piano_only(score: stream.Stream) -> bool:
    """沒標樂器的樂譜也算鋼琴：music21 的預設就是鋼琴。"""
    instruments = list(score.recurse().getElementsByClass(instrument.Instrument))
    return all(isinstance(i, instrument.Piano) for i in instruments)


def render(score: stream.Stream, name: str, play: bool = True):
    """把 score 存成 output/midi/<name>.mid 和 output/wav/<name>.wav，回傳 wav 路徑。"""
    midi_path = midi_utils.MIDI_DIR / f"{name}.mid"
    wav_path = midi_utils.WAV_DIR / f"{name}.wav"

    # 1) music21 直接寫 MIDI
    midi_path.parent.mkdir(parents=True, exist_ok=True)
    score.write("midi", fp=str(midi_path))

    # 2) MIDI→WAV（共用實作）；全鋼琴就自動用 Salamander（Yamaha C5）
    midi_utils.midi_to_wav(midi_path, wav_path, piano_only=_piano_only(score))

    # 3) 試聽
    if play:
        midi_utils.play(wav_path)

    print(f"✓ {midi_path.name}  +  {wav_path.name}")
    return wav_path
