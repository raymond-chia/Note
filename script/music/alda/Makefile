SCORES_DIR := scores
OUTPUT_DIR := output
MIDI_DIR := $(OUTPUT_DIR)/midi
WAV_DIR := $(OUTPUT_DIR)/wav

ALDA_FILES := $(wildcard $(SCORES_DIR)/*.alda)
MIDI_FILES := $(patsubst $(SCORES_DIR)/%.alda,$(MIDI_DIR)/%.mid,$(ALDA_FILES))
WAV_FILES := $(patsubst $(MIDI_DIR)/%.mid,$(WAV_DIR)/%.wav,$(MIDI_FILES))

.PHONY: build wav clean help

help:
	@echo "Available targets:"
	@echo "  make build  - Build all MIDI files from Alda sources"
	@echo "  make wav    - Convert MIDI files to WAV"
	@echo "  make demo   - Play the demo MIDI file"
	@echo "  make clean  - Remove generated files"

build: $(MIDI_FILES)
	@echo "✓ MIDI files built successfully"

wav: $(WAV_FILES)
	@echo "✓ WAV files created successfully"

$(MIDI_DIR)/%.mid: $(SCORES_DIR)/%.alda
	@mkdir -p $(MIDI_DIR)
	alda export -f $< -o $@ -O midi

$(WAV_DIR)/%.wav: $(MIDI_DIR)/%.mid
	@mkdir -p $(WAV_DIR)
	timidity $< -Ow -o $@

demo:
	@echo "Playing demo MIDI file..."
	afplay $(WAV_DIR)/demo.wav

clean:
	rm -rf $(MIDI_DIR) $(WAV_DIR)

.DEFAULT_GOAL := help
