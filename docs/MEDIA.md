# Portfolio media sources

Checked: 2026-10-29T15:50:53.217540+00:00

The media catalogue reads the 33 public capability sites. It selects each main film, reel, lesson or demo from actual HTML sources, prefers MP4 for the player, keeps the original caption track, and records observed transcript and 15-second-cut destinations. Missing optional destinations remain null. The main media bytes continue to be served by their original GitHub Pages projects.

Posters under `assets/posters/` are unchanged copies of the public images, named by capability ID. No video was downloaded, generated, edited or re-rendered. `content/media.json` retains the original URLs and public HTTP checks.

## Scope

{
  "entries": 33,
  "available": 33,
  "posters": 33,
  "kinds": {
    "film": 30,
    "lesson": 1,
    "reel": 1,
    "demo": 1
  },
  "captions": 32,
  "transcripts": 28,
  "cuts": 30,
  "errors": []
}

Decisioncraft has demonstrations rather than a dedicated portfolio film; its entry links the first useful canvas demonstration under `#first-canvas`. Sizzle’s reel uses `#reel`, and Taste × Elegance’s lesson uses `#lesson`. These actual anchors and media labels are preserved. The 28 films across the three recent waves are a separate production scope.

Where a transcript exists inline, its URL points to the observed transcript element on the capability site. Older films without an observed transcript destination retain null rather than a guessed file. Captions and transcript destinations are distinct.

## Production notes supplied by Michael

- All nine wave 3 films were reported live by 11:40 ET on October 29, with every site deploy successful. The three waves total 28 films; Good Teammate’s pull request is merged.
- The user reports the film checks passed, including narration/music targets and scripted-word recognition. Those reports do not substitute for an independent listening review here.
- Build with Tauri still merits a pronunciation listen: recognition heard “Tauri” as “Tari.” A re-voice may be considered after listening.
- Imagen Provider’s end card crops Otto the octopus at the bottom edge. The user identifies it as cosmetic; correcting it requires a re-render. No poster or media crop was changed by this portfolio work.
