# AI Tells — Merged Hard-Ban Reference

A consolidated, scannable list of forbidden patterns merged across the six design archetype skills in this bundle: `design-taste` (base), `gpt-taste`, `minimalist-taste`, `brutalist-taste`, `soft-editorial-taste`, and `redesign-existing-projects`.

Every ban below is **testable in 5 seconds** by visual inspection of the rendered page or grep over the source. No vibes — only checkable rules.

---

## Universal bans (banned across ALL archetypes)

These hold regardless of which archetype overlay is active.

### Typography
- **Inter font — banned as body/UI default.** Use `Geist`, `Outfit`, `Cabinet Grotesk`, or `Satoshi` instead. **Exception:** the `brutalist-taste` archetype may use `Inter` at Black/ExtraBold weight ONLY for macro-typography (e.g., `clamp(4rem, 10vw, 15rem)` headlines) — never for body or UI. (5-sec test: grep `font-family.*Inter` then check weight; flag any non-Black usage.)
- **Roboto, Open Sans, Helvetica, Arial as primary** — same rationale.
- **Title Case On Every Header** — use sentence case.

### Color
- **Pure `#000000`** — use off-black (`#0a0a0a`, `#111111`, `#121212`, Zinc-950).
- **Purple/blue "AI gradient" aesthetic** — the most common AI fingerprint. (5-sec test: grep for `from-purple` or `from-blue.*to-purple`.)
- **Oversaturated accents** — keep saturation < 80%.
- **More than one accent color** — pick one, remove the rest.
- **Mixing warm and cool grays** in the same project.

### Layout
- **`h-screen` for full-height heroes** — use `min-h-[100dvh]` (iOS Safari viewport bug).
- **`window.addEventListener('scroll')`** — use IntersectionObserver or Framer Motion's `whileInView` / `useScroll`. (5-sec test: grep the literal string.)
- **Animating `top`, `left`, `width`, `height`** — animate `transform` and `opacity` only.
- **3-column equal-card "feature row"** — replace with 2-column zig-zag, asymmetric grid, or horizontal scroll.
- **`z-50` / `z-[9999]` spam** — z-indexes only for systemic layers (sticky nav, modals, overlays, tooltips).
- **Complex flexbox percentage math** (`w-[calc(33%-1rem)]`) — use CSS Grid.

### Content
- **Generic placeholder names**: "John Doe", "Jane Smith", "Sarah Chan", "Jack Su". Use realistic, diverse, contextual names.
- **Round fake numbers**: `99.99%`, `50%`, `$100.00`, basic phone numbers like `1234567`. Use organic data: `47.2%`, `+1 (312) 847-1928`.
- **Startup-slop brand names**: "Acme", "Nexus", "SmartFlow", "Flowbit", "Quantumly", "NovaCore". Invent contextual, believable names.
- **AI copywriting clichés**: "Elevate", "Seamless", "Unleash", "Next-Gen", "Game-changer", "Delve", "Tapestry", "Revolutionize", "Transformative platform", "In the world of...". Write plain, specific language.
- **Lorem Ipsum** — never. Write real draft copy.
- **Exclamation marks in success messages** — confident, not loud.
- **"Oops!" error messages** — be direct: "Connection failed. Please try again."

### Imagery & external resources
- **Broken Unsplash links** — use `https://picsum.photos/seed/{keyword}/1920/1080` instead.
- **Stock "diverse team" photos** — use real shots or consistent illustration style.
- **Same avatar image for multiple users**.
- **Generic SVG "egg" or Lucide user icons for avatars**.

### Motion
- **Standard `linear` or `ease-in-out` transitions only** — use custom cubic-bezier or spring physics.
- **Instant state changes without interpolation**.

### Code quality
- **Div soup** — use semantic HTML (`<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`).
- **Import hallucinations** — verify every import exists in `package.json` before using.
- **Missing alt text** on meaningful images.
- **Commented-out dead code** in shipped output.
- **Emojis in code, markup, content, or alt text** — replace with proper icons (Phosphor, Radix, Heroicons).

---

## Archetype-specific bans

These are banned by SOME archetypes and may be allowed (or even required) in others. Note the enforcing archetype.

### Banned by `minimalist-taste` (allowed elsewhere)
- **Gradients of any kind** (minimalist forbids them; soft-skill and brutalist may use radial mesh sparingly).
- **Tailwind heavy drop shadows** (`shadow-md`, `shadow-lg`, `shadow-xl`) — minimalist requires shadow opacity < 0.05; soft-skill *requires* highly diffused ambient shadows.
- **`rounded-full` for large containers / cards / primary buttons** — minimalist forbids; soft-skill *requires* it for nav pills and CTAs.
- **Lucide / Feather / standard Heroicons** — minimalist requires Phosphor Bold/Fill or Radix.
- **3D glassmorphism (beyond subtle navbar blur)** — minimalist forbids; soft-skill `Ethereal Glass` archetype *requires* `backdrop-blur-2xl`.
- **Primary colored backgrounds for large sections** (bright blue/green/red heroes).
- **Neon colors**.

### Banned by `brutalist-taste` (allowed elsewhere)
- **`border-radius`** — brutalist requires exactly 90° corners everywhere.
- **Gradients, soft drop shadows, modern translucency** — banned in brutalist.
- **Mixing Swiss Industrial (light) and Tactical Telemetry (dark) substrates** in the same interface.
- **Serif fonts in dashboards** — brutalist allows serifs *only* sparingly with halftone post-processing; taste-skill bans Serif on dashboards entirely.
- **Mixed-case structural headers** — brutalist requires exclusively uppercase.

### Banned by `soft-editorial-taste` (allowed elsewhere)
- **Standard thick-stroked Lucide / FontAwesome / Material Icons** — soft requires ultra-light lines (Phosphor Light, Remix Line).
- **Generic 1px solid gray borders** — soft requires the "Doppelrand" double-bezel nested architecture.
- **Edge-to-edge sticky navbars glued to the top** — soft requires a floating glass pill detached with `mt-6`.
- **Symmetrical 3-column Bootstrap-style grids without massive whitespace gaps**.
- **Trailing arrow icons sitting naked next to button text** — soft requires the "button-in-button" nested circular wrapper.

### Banned by `gpt-taste` (allowed elsewhere)
- **Cheap meta-labels**: "SECTION 01", "SECTION 04", "QUESTION 05", "ABOUT US" — banned forever in gpt-taste.
- **6-line wrapped hero headlines** — hero H1 must NEVER exceed 2–3 lines (gpt-taste enforces; others recommend).
- **Empty cells in CSS Grid** — gpt-taste mandates `grid-flow-dense` and mathematical interlock.
- **Floating stamp/badge icons on hero text**.
- **Pill-tags under the hero**.
- **Raw data/stats in the hero**.
- **Invisible button text** (dark text on dark background) — universal in spirit, gpt-taste makes it an explicit pre-flight check.

### Banned by `design-taste` base (allowed in some overlays)
- **Centered Hero/H1** when `DESIGN_VARIANCE > 4` — base skill bans; minimalist may center heroes at low variance.
- **Card containers** when `VISUAL_DENSITY > 7` — base skill bans; replace with `border-t`, `divide-y`, or pure spacing.
- **Custom mouse cursors**.
- **Excessive gradient text fills for large headers**.
- **Default `box-shadow` glows / auto-glows** — use inner borders or tinted shadows.
- **Oversized H1s** that "scream" — control hierarchy with weight and color, not scale alone.

### Banned by `redesign-existing-projects` (audit list, project-dependent)
- **`height: 100vh`** — replace with `min-height: 100dvh`.
- **Buttons not bottom-aligned in card groups** when content lengths vary.
- **Feature lists starting at different vertical positions** in pricing tables.
- **Mathematical alignment that looks optically wrong** — icons next to text often need 1–2px optical adjustment.
- **Random dark sections breaking an otherwise light page** (or vice versa) — copy-paste accident look.
- **Empty flat sections with no visual depth** — add background imagery, ambient gradients, or subtle patterns.
- **Symmetrical vertical padding** — bottom often needs to be slightly larger than top.
- **Always-left sidebar dashboards** — try top nav, command menu, or collapsible panel.
- **Pricing table with 3 towers** — highlight recommended tier with color and emphasis, not just height.
- **Dead links** (`href="#"`).
- **No "skip to content" link**.
- **Light/dark toggle as sun/moon switch only**.

---

## How to apply

1. The **Universal bans** section above acts as a baseline pre-flight check on every design output, regardless of archetype.
2. The **Archetype-specific bans** apply when the named archetype overlay is active. If two overlays disagree (e.g., minimalist forbids `rounded-full` for cards but soft requires it for nav pills), the most-recently-loaded overlay wins.
3. Every ban here is a checkable rule. If a rule cannot be tested in 5 seconds by either visual inspection or grep, it does not belong on this list.
