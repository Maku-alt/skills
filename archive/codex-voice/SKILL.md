---
name: codex-voice
description: Global voice layer for Codex on Windows. Use when you want audio conversation in VSCode or CLI with hotkey, local transcription (faster-whisper), autosend, clipboard fallback, and daemon troubleshooting.
---

# Codex Voice

## Quick Use

1. `codex-voice status`
2. `codex-voice start` (if not running)
3. Hotkey `Ctrl+Shift+V`:
- one tap starts recording
- second tap or silence cuts and processes

## Key Commands

- `codex-voice setup`
- `codex-voice doctor`
- `codex-voice mode set autosend`
- `codex-voice mode set one_enter`
- `codex-voice session pin-current`
- `codex-voice session set auto`
- `codex-voice session show`
- `codex-voice test stt`
- `codex-voice test tts`
- `codex-voice stop`

## Troubleshooting

- Logs:
  - `C:\Users\Victor\.codex\voice\logs\events.jsonl`
  - `C:\Users\Victor\.codex\voice\logs\errors.jsonl`
- Last response text:
  - `C:\Users\Victor\.codex\voice\latest_response.txt`
- If autosend fails, transcript is copied to clipboard.
- Use a headset to reduce echo.
