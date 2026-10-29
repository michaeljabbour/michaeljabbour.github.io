# Add the overview film

When “Good Work Has a Next Day” is ready, place its final web MP4, poster, English VTT and transcript under `assets/overview/`, or use their stable public HTTPS URLs.

Create `content/home-film.json`:

```json
{
  "title": "Good Work Has a Next Day",
  "src": "assets/overview/portfolio.mp4",
  "poster": "assets/overview/portfolio-poster.jpg",
  "caption": "assets/overview/portfolio.vtt",
  "transcript": "assets/overview/transcript.html"
}
```

Rebuild and run the checks. This replaces the homepage’s three-project artwork composition with a native, captioned overview player. It does not autoplay. With this file absent, the complete portfolio remains visible and usable.

A poster and caption track are required when `src` is supplied. A transcript is optional in the configuration but should accompany the final film. Use stable destinations and keep every public filename free of personal or internal data.

## Connected (October 29, 2026)

The film is in place: `assets/overview/portfolio.mp4` (web encode, 90 s, about 9 MB), `portfolio-poster.jpg` (the "Where do I start?" moment), `portfolio.vtt` (captions from the narration) and a transcript page at `assets/overview/transcript/`. The checker counts that transcript page as a 39th HTML page only when it exists. The project shown in the film, Bramble & Bolt, is fictional, and the film makes no outcome claims.
