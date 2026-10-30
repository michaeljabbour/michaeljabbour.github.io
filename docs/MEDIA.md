# Portfolio media sources

The media catalogue reads the 33 public capability sites. It selects each main film, reel, lesson or demo from actual HTML sources, prefers MP4 for the player, keeps the original caption track, and records observed transcript and 15-second-cut destinations. Missing optional destinations remain null. The main media bytes continue to be served by their original GitHub Pages projects.

Posters under `assets/posters/` are unchanged copies of the public images, named by capability ID. No video was downloaded, generated, edited or re-rendered. `content/media.json` retains the original URLs and public HTTP checks.

Decisioncraft has demonstrations rather than a dedicated portfolio film; its entry links the first useful canvas demonstration under `#first-canvas`. Sizzle’s reel uses `#reel`, and Taste × Elegance’s lesson uses `#lesson`. These actual anchors and media labels are preserved.

Where a transcript exists inline, its URL points to the observed transcript element on the capability site. Older films without an observed transcript destination retain null rather than a guessed file. Captions and transcript destinations are distinct.

## Film stills

`assets/stills/` holds one frame from each of the 28 capability films produced in October 2026, taken unchanged from the film's own master render at a representative moment (usually the showpiece). `content/media.json` names each one as `still`; the build uses it for thumbnails and as the player poster, and falls back to the copied end-card poster for the five entries without one (Market Fit, Decisioncraft, Taste × Elegance, Worth Using, Sizzle). No still is generated, retouched or composited.
