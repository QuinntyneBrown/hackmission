"""Build the 20-second HackMission intro video.

Inputs  hackmission-intro.txt       one narrated line per slide
        upbeat-and-inspiring.mp3    "Upbeat And Inspiring" (AtlasAudio, Pixabay), mixed under the voice
        kokoro/                     Kokoro-82M ONNX + am_fenrir voice from Hugging Face (auto-downloaded)
Outputs hackmission-intro.mp4, hackmission-intro.vtt, hackmission-intro-poster.png

Needs: kokoro-onnx, onnxruntime, huggingface_hub, numpy, ffmpeg/ffprobe, python playwright (chromium).
Run:   python -I build_video.py  (from any directory)
"""
import pathlib, shutil, subprocess, tempfile, wave

import numpy as np
import onnxruntime as ort
from huggingface_hub import hf_hub_download
from kokoro_onnx.tokenizer import Tokenizer
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
HF_REPO, VOICE, SPEED = "onnx-community/Kokoro-82M-v1.0-ONNX", "am_fenrir", 1.08
MUSIC, MUSIC_DB, MUSIC_START = HERE / "upbeat-and-inspiring.mp3", -11, 30.0  # skip the quiet intro
LEAD, GAP, TAIL = 0.5, 0.3, 1.6   # seconds before, between and after lines (tail lets the music ring out)
LINES = HERE.joinpath("hackmission-intro.txt").read_text(encoding="utf-8").splitlines()

MARK = ('<svg viewBox="0 0 64 64" fill="none" width="{s}" height="{s}">'
        '<path d="M21 9C15 9 14.5 13 14.5 19V25C14.5 29 12.5 32 8 32C12.5 32 14.5 35 14.5 39V45C14.5 51 15 55 21 55" stroke="#F7F4EE" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M43 9C49 9 49.5 13 49.5 19V25C49.5 29 51.5 32 56 32C51.5 32 49.5 35 49.5 39V45C49.5 51 49 55 43 55" stroke="#F7F4EE" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
        '<rect x="29" y="14" width="6" height="36" rx="1.5" fill="#E8A33D"/><rect x="21.5" y="23" width="21" height="6" rx="1.5" fill="#E8A33D"/></svg>')
SLIDES = [
    ('<p class="k">{ every season }</p><h1>Coders, designers<br>&amp; dreamers<br><em>across Canada.</em></h1>'),
    ('<p class="k">{ 48 hours }</p><h1>Real problems from<br><em>churches, charities<br>&amp; communities.</em></h1>'),
    (f'{MARK.format(s=260)}<h1 style="margin-top:40px">Code in service of<br><em>the mission.</em></h1>'),
    (f'<div class="lock">{MARK.format(s=200)}<span><b>Hack</b>Mission</span></div>'
     '<p class="cta">Get on the list → <em>hackmission.ca</em></p>'),
]
CSS = """@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;700;800&display=swap');
html,body{margin:0;width:1920px;height:1080px;background:radial-gradient(circle at 25% 15%,#1d3a70,#0B1B3A 55%,#07122a);color:#F7F4EE;font-family:Manrope,sans-serif}
body{display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}
h1{font-size:112px;font-weight:800;letter-spacing:-.035em;line-height:1.05;margin:0}
em{font-style:normal;color:#E8A33D}.k{font:700 44px ui-monospace,Consolas,monospace;color:#E8A33D;margin:0 0 36px}
.lock{display:flex;align-items:center;gap:44px;font-size:150px;letter-spacing:-.035em}.lock b{font-weight:800}.lock span{font-weight:500}
.cta{font-size:56px;font-weight:700;margin-top:56px}"""


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)]).strip())


def ts(t):
    return f"{int(t // 3600):02}:{int(t % 3600 // 60):02}:{t % 60:06.3f}"


class Narrator:
    """Kokoro-82M via onnxruntime; model and voice come from Hugging Face on first run."""

    def __init__(self):
        k = HERE / "kokoro"
        k.mkdir(exist_ok=True)
        for sub, name in (("onnx", "model.onnx"), ("voices", f"{VOICE}.bin")):
            if not (k / name).exists():
                shutil.copy(hf_hub_download(HF_REPO, f"{sub}/{name}"), k / name)
        self.tok = Tokenizer()
        self.sess = ort.InferenceSession(str(k / "model.onnx"))
        self.style = np.fromfile(k / f"{VOICE}.bin", dtype=np.float32).reshape(-1, 1, 256)

    def say(self, text, out):
        ids = self.tok.tokenize(self.tok.phonemize(text, lang="en-us"))
        audio = self.sess.run(None, {"input_ids": np.array([[0, *ids, 0]], dtype=np.int64),
                                     "style": self.style[len(ids)],
                                     "speed": np.array([SPEED], dtype=np.float32)})[0].reshape(-1)
        audio = np.trim_zeros(np.where(np.abs(audio) < 0.004, 0, audio))  # trim leading/trailing silence
        with wave.open(str(out), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000)
            w.writeframes((np.clip(audio, -1, 1) * 32767).astype(np.int16).tobytes())


def main():
    tmp = pathlib.Path(tempfile.mkdtemp())
    narrator = Narrator()
    voices = []
    for i, line in enumerate(LINES):
        out = tmp / f"v{i}.wav"
        narrator.say(line, out)
        voices.append((line, out, dur(out)))

    # Timeline: each slide starts with its line; the last slide holds for TAIL.
    starts, t = [], LEAD
    for _, _, d in voices:
        starts.append(t)
        t += d + GAP
    total = t - GAP + TAIL
    slide_d = [(starts[i + 1] if i + 1 < len(starts) else total) - (0 if i == 0 else starts[i]) for i in range(len(starts))]

    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1920, "height": 1080})
        for i, html in enumerate(SLIDES):
            pg.set_content(f"<style>{CSS}</style>{html}")
            pg.wait_for_timeout(600)
            pg.screenshot(path=str(tmp / f"s{i}.png"))
        b.close()
    shutil.copy(tmp / "s2.png", HERE / "hackmission-intro-poster.png")

    # Narration track: voice clips placed at their start times.
    inputs, filt = [], []
    for i, (_, p, _) in enumerate(voices):
        inputs += ["-i", str(p)]
        ms = int(starts[i] * 1000)
        filt.append(f"[{i}:a]adelay={ms}|{ms}[a{i}]")
    filt.append("".join(f"[a{i}]" for i in range(len(voices))) + f"amix=inputs={len(voices)}:normalize=0,apad,atrim=0:{total:.3f}[voice]")
    n = len(voices)
    if not MUSIC.exists():
        raise SystemExit(f"{MUSIC.name} is missing — every HackMission video has music under it (see README.md)")
    inputs += ["-i", str(MUSIC)]
    filt.append(f"[{n}:a]atrim={MUSIC_START}:{MUSIC_START + total:.3f},asetpts=PTS-STARTPTS,volume={MUSIC_DB}dB,afade=t=in:d=0.8,afade=t=out:st={total - 2.5:.3f}:d=2.5[bg];"
                "[voice]volume=1.6,alimiter=limit=0.95[vx];[vx][bg]amix=inputs=2:normalize=0,alimiter=limit=0.97[aout]")
    n += 1

    # Video: slides with crossfades.
    for i in range(len(SLIDES)):
        inputs += ["-loop", "1", "-t", f"{slide_d[i] + 0.5:.3f}", "-i", str(tmp / f"s{i}.png")]
    xf, prev, off = [], f"[{n}:v]", 0.0
    for i in range(1, len(SLIDES)):
        off += slide_d[i - 1]
        xf.append(f"{prev}[{n + i}:v]xfade=transition=fade:duration=0.5:offset={off - 0.25:.3f}[x{i}]")
        prev = f"[x{i}]"
    filt += xf
    filt.append(f"{prev}fade=t=in:d=0.4,fade=t=out:st={total - 0.6:.3f}:d=0.6,format=yuv420p[vout]")

    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt),
                           "-map", "[vout]", "-map", "[aout]", "-t", f"{total:.3f}", "-r", "30",
                           "-c:v", "libx264", "-crf", "22", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
                           str(HERE / "hackmission-intro.mp4")])

    vtt = ["WEBVTT", ""]
    for i, (line, _, d) in enumerate(voices):
        vtt += [f"{ts(starts[i])} --> {ts(starts[i] + d)}", line, ""]
    (HERE / "hackmission-intro.vtt").write_text("\n".join(vtt), encoding="utf-8")
    print(f"built {total:.1f}s video")


if __name__ == "__main__":
    main()
