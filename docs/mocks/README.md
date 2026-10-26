# HackMission — marketing site mocks

Static HTML mocks for the HackMission marketing page: a Canadian
hackathon that runs several times a year. The page's job is to get visitors onto
the mailing list so they hear when the next event opens.

<!--
Cast & catalog (reuse in every mock)
  Today: Mon 26 Oct 2026
  Subscriber: Amara Okafor, amara.okafor@example.ca
  2027 season: Toronto 6–7 Feb (reg. opens 15 Dec 2026) · Vancouver 17–18 Apr ·
               Montréal 12–13 Jun (bilingual) · Halifax + online 25–26 Sep
  Contact: hello@hackmission.ca · privacy@hackmission.ca
-->

## Open the mocks

Open `index.html` from disk. Append `?theme=dark` to force dark, `?chrome=0` to
hide the mock bar and notes.

## Brand

From the Magic Patterns spec: ink `#0B1B3A`, gold `#E8A33D`, paper `#F7F4EE`,
Manrope 500/700/800. LogoMark is code braces `{ }` framing a gold cross; the
lockup is **Hack**Mission (extrabold + medium). Brand tokens and marketing
components are in `assets/brand.css`, layered over `tokens.css` and `ui.css`.

## Layout rhythm

Inspired by yfc.ca: one idea per section, ~150 words on the whole home page, three or four words per headline line,
section padding of 6–10 rem, and a single button per section. The home page
runs hero → offset card (paper card straddling the ink hero) → numbers row →
three steps → one-line statement with a diagonal ink panel → season → two-question FAQ. Headlines
carry the message; body copy is one sentence or less.

## Intro video

`assets/media/hackmission-intro.mp4` is a 20-second, 1080p narrated video with
optional captions (`hackmission-intro.vtt`, off by default) and a poster. The narrator is **Kokoro-82M**
(voice `am_fenrir`) from Hugging Face, run locally with onnxruntime; the script
is `hackmission-intro.txt`.

Background music: **"Upbeat And Inspiring" by AtlasAudio from Pixabay**
(Pixabay Content License), mixed under the voice at −11 dB with fades. Full
provenance is in `assets/media/README.md`. Rebuild with
`python -I docs/mocks/assets/media/build_video.py`; the build refuses to run
without the music track.

## Requirements (assumed — no docs/specs yet)

| ID | Requirement |
|---|---|
| MKT-01 | Visitors can join a mailing list to be notified of the next hackathon (double opt-in, CASL). |
| MKT-02 | The home page offers a ~20 s narrated intro video with music, captions and a transcript. |
| MKT-03 | The home page shows the next event date, or says one is coming when none is announced. |
| MKT-04 | Subscribers confirm via an emailed link; expired links offer a resend. |
| MKT-05 | Every email has a one-click unsubscribe. |
| MKT-06 | A plain-language privacy page (PIPEDA). |

## Open questions

- Event cities and dates above are placeholders — confirm the real 2027 season.
- Is French (Montréal event) a full `/fr` site, or bilingual copy on one page?
- Minimum age (assumed 16+ with guardian consent under 18).
- Manrope loads from Google Fonts; self-host it for production and offline mocks.

## Re-check and re-screenshot

```sh
python .claude/skills/writing-html-mocks/scripts/check_mocks.py docs/mocks --write
python .claude/skills/writing-html-mocks/scripts/screenshot_mocks.py docs/mocks
```

## Coverage

<!-- coverage:start -->

Legend: ✅ mock exists · ➖ not applicable (reason in manifest) · ❌ missing

### Pages

| Screen | default | loading | empty | error | submitting | invalid | success | already-subscribed | Requirements |
|---|---|---|---|---|---|---|---|---|---|
| Home (`home`) | [✅](pages/home/default.html) | ➖ | [✅](pages/home/empty.html) | [✅](pages/home/error.html) | [✅](pages/home/submitting.html) | [✅](pages/home/invalid.html) | [✅](pages/home/success.html) | [✅](pages/home/already-subscribed.html) | `MKT-01`, `MKT-02`, `MKT-03` |
| Confirm subscription (`confirm`) | [✅](pages/confirm/default.html) | [✅](pages/confirm/loading.html) | ➖ | [✅](pages/confirm/error.html) |  |  |  |  | `MKT-04` |
| Unsubscribe (`unsubscribe`) | [✅](pages/unsubscribe/default.html) | ➖ | ➖ | [✅](pages/unsubscribe/error.html) | [✅](pages/unsubscribe/submitting.html) |  | [✅](pages/unsubscribe/success.html) |  | `MKT-05` |
| Privacy (`privacy`) | [✅](pages/privacy/default.html) | ➖ | ➖ | ➖ |  |  |  |  | `MKT-06` |
| Page not found (`not-found`) | [✅](pages/not-found/default.html) | ➖ | ➖ | ➖ |  |  |  |  |  |

### Dialogs

| Screen | default | busy | invalid | loading | error | Requirements |
|---|---|---|---|---|---|---|
| Watch the 20-second intro (`video`) | [✅](dialogs/video/default.html) | ➖ | ➖ | [✅](dialogs/video/loading.html) | [✅](dialogs/video/error.html) | `MKT-02` |

### Notifications

| Screen | info | success | warning | danger | Requirements |
|---|---|---|---|---|---|
| Signup toast (`signup-toast`) | [✅](notifications/signup-toast/info.html) | [✅](notifications/signup-toast/success.html) | ➖ | [✅](notifications/signup-toast/danger.html) | `MKT-01` |

<!-- coverage:end -->
