# Intro video media

| File | What | Source | License |
| --- | --- | --- | --- |
| `upbeat-and-inspiring.mp3` | _Upbeat And Inspiring_ by AtlasAudio (3:16) — background music | [pixabay.com/music/upbeat-upbeat-and-inspiring-578932](https://pixabay.com/music/upbeat-upbeat-and-inspiring-578932/) | [Pixabay Content License](https://pixabay.com/service/license-summary/): free for commercial use, no attribution required |
| `kokoro/model.onnx`, `kokoro/am_fenrir.bin` | Kokoro-82M text-to-speech, voice `am_fenrir` — the narrator | [huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX](https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX) (weights from [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)) | Apache-2.0 |
| `hackmission-intro.txt` | Narration script, one line per slide | — | — |
| `hackmission-intro.mp4`, `.vtt`, `-poster.png` | Built outputs of `build_video.py` | — | — |

Rebuild: `python -I docs/mocks/assets/media/build_video.py` (needs ffmpeg, python `playwright` with Chromium, `kokoro-onnx`, `huggingface_hub`). If the `kokoro/` files are missing the script downloads them from Hugging Face.
