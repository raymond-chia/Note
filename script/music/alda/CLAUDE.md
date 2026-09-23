# Alda Cheat Sheet（完整語法）

> 如果你自己試這些範例卻聽不到聲音，請先指定樂器，例如：

```alda
piano: c d e f g
```

> 在 REPL session 中宣告過樂器之後，該樂器會維持為 active，不需要每次重複指定。

---

## 目錄

- [Alda Cheat Sheet（完整語法）](#alda-cheat-sheet完整語法)
  - [目錄](#目錄)
  - [Comments](#comments)
  - [Notes](#notes)
  - [Rests](#rests)
  - [Octaves](#octaves)
  - [Accidentals](#accidentals)
  - [Note lengths / duration](#note-lengths--duration)
  - [Ties](#ties)
  - [Slurs / legato](#slurs--legato)
  - [Cram expressions](#cram-expressions)
  - [Chords](#chords)
  - [Voices](#voices)
  - [Parts](#parts)
  - [Tempo](#tempo)
  - [Volume / dynamics](#volume--dynamics)
  - [Panning](#panning)
  - [Quantization (legato \<-\> staccato)](#quantization-legato---staccato)
  - [Key signature](#key-signature)
  - [Markers](#markers)
  - [Variables](#variables)
  - [Repeats](#repeats)
- [List of Instruments](#list-of-instruments)
  - [MIDI Instruments](#midi-instruments)
    - [Piano](#piano)
    - [Chromatic Percussion](#chromatic-percussion)
    - [Organ](#organ)
    - [Guitar](#guitar)
    - [Bass](#bass)
    - [Strings (and Timpani, for some reason)](#strings-and-timpani-for-some-reason)
    - [Ensemble](#ensemble)
    - [Brass](#brass)
    - [Reed](#reed)
    - [Pipe](#pipe)
    - [Synth Lead](#synth-lead)
    - [Synth Pad](#synth-pad)
    - [Synth Effects](#synth-effects)
    - [Ethnic](#ethnic)
    - [Percussive](#percussive)
    - [Sound Effects](#sound-effects)
    - [Percussion](#percussion)

---

## Comments

```alda
# This is a comment.
piano: c   # This is also a comment.
```

## Notes

```alda
c d e f g
```

## Rests

```alda
c r d r e r f r g
```

## Octaves

Explicit octave numbers:

```alda
o0 c o1 c o2 c o3 c o4 c o5 c o6 c o7 c o8 c o9 c

o4 g a b o5 c o4 b a g
```

Octave up (`>`) and down (`<`):

```alda
o0 c > c > c > c > c > c > c > c > c > c

o4 g a b > c < b a g
```

## Accidentals

Sharps (`+`) and flats (`-`):

```alda
c < b- a g f+
```

Double flats/sharps:

```alda
g+ f+ e+ d+ c++
```

The sky is the limit!:

```alda
c++++-+-+-+
```

## Note lengths / duration

Standard “powers of two” note lengths (quarter, eighth, etc.):

```alda
c4 c8 c c16 c c c c32 c c c c c c c | c1
```

Dotted notes:

```alda
c4 c4
c4. c8
c4.. c16
c4... c32
c2. c4
```

Non-standard note lengths:

```alda
c9 c8 c7 c6 c5 c4 c3 c2 c1
```

Second (`s`) and millisecond (`ms`) note durations:

```alda
c2s d522ms e1234ms f5s
```

## Ties

```alda
g+1~1

c2.~500ms~4..
```

## Slurs / legato

```alda
c4~ d~ e~ f
```

## Cram expressions

```alda
{c}2
{c d}2
{c d e}2
{c d e f}2
{c d e f g}2
{c d e f g a}2
{c d e f g a}4 {c d e f g a}4 {d e f g a b}4 > c2
```

Nested cram expressions:

```alda
{c {d {d+ e} f f+} g a}1
```

## Chords

```alda
c1/e-/g/b

c1/e/g/>c4 < b a g | < g+1/b/>e
```

## Voices

```alda
V1: c8 d e f g a b > c1
V2: e8 f g a b > c d e1
V3: g8 a b > c d e f g1
V4: o3 c2 g4 < g8 c1
```

## Parts

```alda
oboe:
	c8 d e f g a b > c1

clarinet:
	e8 f g a b > c d e1

flute:
	g8 a b > c d e f g1

bassoon:
	o3 c2 g4 < g8 c1
```

Named parts:

```alda
cello "my-cello-1":
	o2 c1~1

cello "my-cello-2":
	r2 o2 g2~1

cello "my-cello-3":
	r1 o3 e1

my-cello-1:
	d2 e f1

my-cello-2:
	a2 b > c1

my-cello-3:
	f2 g a1
```

Part groups:

```alda
violin/viola/cello "strings":
	g1

strings:
	e

strings.violin:
	> c

strings.viola:
	e

strings.cello:
	< c
```

## Tempo

**Local** tempo (only affects the current part):

```alda
trumpet:
	(tempo 200) o4 c8 d e f g a b > c4.

trombone:
	o3 e8 f g a b > c d e4.
```

**Global** tempo (affects all parts):

```alda
trumpet:
	(tempo! 200) o4 c8 d e f g a b > c4.

trombone:
	o3 e8 f g a b > c d e4.
```

You can also declare a global tempo at the top of the score:

```alda
(tempo! 150)

clarinet:
	c d e

flute:
	e f g
```

## Volume / dynamics

Dynamic markings:

```alda
(pppppp) c
(ppppp) c
(pppp) c
(ppp) c
(pp) c
(p) c
(mp) c
(mf) c
(f) c
(ff) c
(fff) c
(ffff) c
(fffff) c
(ffffff) c
```

Explicit volume level (0-100):

```alda
(vol 20) c
(vol 35) c
(vol 57) c
(vol 75) c
(vol 89) c
(vol 100) c
```

## Panning

```alda
piano:
	(panning 0)   c8
	(panning 15)  d
	(panning 30)  e
	(panning 45)  f
	(panning 60)  g
	(panning 75)  a
	(panning 90)  b
	(panning 100) > c

	V1: (panning 0)
		o2 g2/>c/e < a-/>c/f < g1/>c/e

	V2: (panning 100)
		o4 r4 c2/e/g c4/f/a- c1/e/g
```

## Quantization (legato <-> staccato)

```alda
bassoon:
	o2 d8 e (quant 30) f+ g (quant 99) a2
```

## Key signature

Major and minor keys:

```alda
(key-sig! '(d major))
o4 d8 e f g a b > c d

(key-sig! '(d minor))
o4 d8 e f g a b > c d
```

Sharp/flat keys:

```alda
(key-sig! '(b flat major))
o3 b8 > c d e f g a b

(key-sig! '(c sharp major))
o4 c8 d e f g a b > c
```

Modes:

```alda
(key-sig! '(d ionian))
o4 d8 e f g a b > c d

(key-sig! '(d dorian))
o4 d8 e f g a b > c d

(key-sig! '(d phrygian))
o4 d8 e f g a b > c d

(key-sig! '(d lydian))
o4 d8 e f g a b > c d

(key-sig! '(d mixolydian))
o4 d8 e f g a b > c d

(key-sig! '(d aeolian))
o4 d8 e f g a b > c d

(key-sig! '(d locrian))
o4 d8 e f g a b > c d
```

Custom key signatures:

```alda
(key-sig! "f+ b- d+")
o4 c8 d e f g a b > c

(key-sig! '(f (sharp) b (flat) d (sharp)))
o4 c8 d e f g a b > c
```

## Markers

```alda
trumpet:
	o4 c8 d e f g a b > %last-note c4.~2

trombone:
	o3 e8 f g a b > c d e4.~2

tuba:
	@last-note o2 c4.~2
```

## Variables

Define riffs/motifs:

```alda
(tempo! 200)

riff = b4 b8 > d4 d8 e4 <

electric-bass:
	o1 riff *4

electric-guitar-distorted:
	o2 riff *4
```

Define your own shorthand:

```alda
quiet  = (vol 25)
loud   = (vol 50)
louder = (vol 75)

notes  = c d e

piano:
	quiet notes
	loud notes
	louder notes
```

Multi-line variable definition:

```alda
(key-sig! '(a flat major))
(tempo! 90)

cocoon = [
	a4 > c8 e g8. e g8 <
	a8. > c e8~2 <
]

midi-synth-pad-new-age:
	(quant 95)
	o2 cocoon *2
```

## Repeats

Repeat a note:

```alda
c *4
```

Repeat a chord:

```alda
c/e/g *4
```

Repeat a sequence:

```alda
[c16 d e f]*3 g2
```

Repeat a variable:

```alda
run = c16 d e f
run*3 g2
```

Repeat with variations:

```alda
[
	o4
	c16 '1,4
	d16 '2,5
	e16 '3,6
	f16 '7-8
	g16 '9

	o3 c16 c c
]*9

o4 a1
```

# List of Instruments

Currently, only General MIDI instruments are supported. In the future, we plan to add [waveform synthesis](https://github.com/alda-lang/alda/issues/100) so that you will be able to use sine/square/triangle/sawtooth waves as well as complex synthesizers built from waveforms.

Any of the instrument names below, as well as their aliases, can be used as instruments in an Alda score, e.g.:

```alda
midi-harpsichord: c8 d e f g a b > c
```

## MIDI Instruments

These directly correspond to the instruments in the [General MIDI sound set](http://www.midi.org/techspecs/gm1sound.php). They are grouped here by patch group according to the MIDI spec.

Aliases are in parentheses after the instrument's name.

> Note that some of these aliases may be replaced in the future with non-MIDI instruments, e.g. sampled or waveform instruments. To ensure that your scores will always use specifically MIDI instruments, you can use the `midi-` prefixed names.

### Piano

- midi-acoustic-grand-piano (midi-piano, piano)
- midi-bright-acoustic-piano
- midi-electric-grand-piano
- midi-honky-tonk-piano
- midi-electric-piano-1
- midi-electric-piano-2
- midi-harpsichord (harpsichord)
- midi-clavi (midi-clavinet, clavinet)

### Chromatic Percussion

- midi-celesta (celesta, celeste, midi-celeste)
- midi-glockenspiel (glockenspiel)
- midi-music-box (music-box)
- midi-vibraphone (vibraphone, vibes, midi-vibes)
- midi-marimba (marimba)
- midi-xylophone (xylophone)
- midi-tubular-bells (tubular-bells)
- midi-dulcimer (dulcimer)

### Organ

- midi-drawbar-organ
- midi-percussive-organ
- midi-rock-organ
- midi-church-organ (organ)
- midi-reed-organ
- midi-accordion (accordion)
- midi-harmonica (harmonica)
- midi-tango-accordion

### Guitar

- midi-acoustic-guitar-nylon (midi-acoustic-guitar, acoustic-guitar, guitar)
- midi-acoustic-guitar-steel
- midi-electric-guitar-jazz
- midi-electric-guitar-clean (electric-guitar-clean)
- midi-electric-guitar-palm-muted
- midi-electric-guitar-overdrive (electric-guitar-overdrive)
- midi-electric-guitar-distorted (electric-guitar-distorted)
- midi-electric-guitar-harmonics (electric-guitar-harmonics)

### Bass

- midi-acoustic-bass (acoustic-bass, upright-bass)
- midi-electric-bass-finger (electric-bass-finger, electric-bass)
- midi-electric-bass-pick (electric-bass-pick)
- midi-fretless-bass (fretless-bass)
- midi-bass-slap
- midi-bass-pop
- midi-synth-bass-1
- midi-synth-bass-2

### Strings (and Timpani, for some reason)

- midi-violin (violin)
- midi-viola (viola)
- midi-cello (cello)
- midi-contrabass (string-bass, arco-bass, double-bass, contrabass, midi-string-bass, midi-arco-bass, midi-double-bass)
- midi-tremolo-strings
- midi-pizzicato-strings
- midi-orchestral-harp (harp, orchestral-harp, midi-harp)
- midi-timpani (timpani)

### Ensemble

- midi-string-ensemble-1
- midi-string-ensemble-2
- midi-synth-strings-1
- midi-synth-strings-2
- midi-choir-aahs
- midi-voice-oohs
- midi-synth-voice
- midi-orchestra-hit

### Brass

- midi-trumpet (trumpet)
- midi-trombone (trombone
- midi-tuba (tuba)
- midi-muted-trumpet
- midi-french-horn (french-horn)
- midi-brass-section
- midi-synth-brass-1
- midi-synth-brass-2

### Reed

- midi-soprano-saxophone (midi-soprano-sax, soprano-saxophone, soprano-sax)
- midi-alto-saxophone (midi-alto-sax, alto-saxophone, alto-sax)
- midi-tenor-saxophone (midi-tenor-sax, tenor-saxophone, tenor-sax)
- midi-baritone-saxophone (midi-baritone-sax, midi-bari-sax, baritone-saxophone, baritone-sax, bari-sax)
- midi-oboe (oboe)
- midi-english-horn (english-horn)
- midi-bassoon (bassoon)
- midi-clarinet (clarinet)

### Pipe

- midi-piccolo (piccolo)
- midi-flute (flute)
- midi-recorder (recorder)
- midi-pan-flute (pan-flute)
- midi-bottle (bottle)
- midi-shakuhachi (shakuhachi)
- midi-whistle (whistle)
- midi-ocarina (ocarina)

### Synth Lead

- midi-square-lead (square, square-wave, square-lead, midi-square, midi-square-wave)
- midi-saw-wave (sawtooth, saw-wave, saw-lead, midi-sawtooth, midi-saw-lead)
- midi-calliope-lead (calliope-lead, calliope, midi-calliope)
- midi-chiffer-lead (chiffer-lead, chiffer, chiff, midi-chiffer, midi-chiff)
- midi-charang (charang)
- midi-solo-vox
- midi-fifths (midi-sawtooth-fifths)
- midi-bass-and-lead (midi-bass+lead)

### Synth Pad

- midi-synth-pad-new-age (midi-pad-new-age, midi-new-age-pad)
- midi-synth-pad-warm (midi-pad-warm, midi-warm-pad)
- midi-synth-pad-polysynth (midi-pad-polysynth, midi-polysynth-pad)
- midi-synth-pad-choir (midi-pad-choir, midi-choir-pad)
- midi-synth-pad-bowed (midi-pad-bowed, midi-bowed-pad, midi-pad-bowed-glass, midi-bowed-glass-pad)
- midi-synth-pad-metallic (midi-pad-metallic, midi-metallic-pad, midi-pad-metal, midi-metal-pad)
- midi-synth-pad-halo (midi-pad-halo, midi-halo-pad)
- midi-synth-pad-sweep (midi-pad-sweep, midi-sweep-pad)

### Synth Effects

- midi-fx-rain (midi-fx-ice-rain, midi-rain, midi-ice-rain)
- midi-fx-soundtrack (midi-soundtrack)
- midi-fx-crystal (midi-crystal)
- midi-fx-atmosphere (midi-atmosphere)
- midi-fx-brightness (midi-brightness)
- midi-fx-goblins (midi-fx-goblin, midi-goblins, midi-goblin)
- midi-fx-echoes (midi-fx-echo-drops, midi-echoes, midi-echo-drops)
- midi-fx-sci-fi (midi-sci-fi)

### Ethnic

- midi-sitar (sitar)
- midi-banjo (banjo)
- midi-shamisen (shamisen)
- midi-koto (koto)
- midi-kalimba (kalimba)
- midi-bagpipes (bagpipes)
- midi-fiddle
- midi-shehnai (shehnai, shahnai, shenai, shanai, midi-shahnai, midi-shenai, midi-shanai)

### Percussive

- midi-tinkle-bell (midi-tinker-bell)
- midi-agogo
- midi-steel-drums (midi-steel-drum, steel-drums, steel-drum)
- midi-woodblock
- midi-taiko-drum
- midi-melodic-tom
- midi-synth-drum
- midi-reverse-cymbal

### Sound Effects

- midi-guitar-fret-noise
- midi-breath-noise
- midi-seashore
- midi-bird-tweet
- midi-telephone-ring
- midi-helicopter
- midi-applause
- midi-gunshot (midi-gun-shot)

### Percussion

There is a special `midi-percussion` instrument (alias: `percussion`) which provides a variety of percussion sounds, each mapped to a different note. Each note corresponds to a unique percussive instrument, but the sound's pitch is not relative to the pitch of the note. (See [here](https://en.wikipedia.org/wiki/General_MIDI#Percussion) for more information about MIDI percussion.)

Drum set example:

```alda
(tempo! 150)

midi-percussion:
  V1: # bass and snare
    o2 c4 e8 c r c e c
  V2: # cymbals (hi-hat, crash, ride bell, another crash)
    o2 f+8 f+ r o3 c+8~8 f16 f r8 a
```
