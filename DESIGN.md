# Michael Jabbour portfolio

The visitor should understand what Michael makes, find a capability for their current work, see it explained in a film, and reach its installation guide or source. The collection includes 33 public capabilities. The private learning experiment and owner-only audit do not belong here.

## Direction

A bright, precise maker's portfolio, with real film artwork as the visual material. One large typographic introduction sits beside a small composition of film stills. The rest of the site uses clear reading order, generous space and compact project lists. A home page introduces the work; a library, film index and individual pages make it explorable. The user is producing the umbrella film separately; nothing pretends it is available.

## Tokens

- Paper `#f5f7fa`, white `#ffffff`, ink `#182f40`, secondary `#536675`, blue `#2453d6`, yellow `#ecf28b`.
- Display: Avenir Next with a system sans fallback. Body: the system sans stack. No external font service.
- Display sizes grow from 42px on phones to about 88px on wide screens. Body is 17–19px with 1.6 line height and a 65-character reading measure.
- Content max width 1240px, generous gutters, left alignment. Film artwork keeps its own palette and 16:9 framing.

## Composition

Home: name/navigation → proposition + film composition → practical entry paths → six selected capabilities → short statement of working principles → full library invitation.

Library: introduction → search + task and format filters → readable thumbnail/title/benefit rows → no-results recovery. Filters work in the URL and are keyboard accessible.

Capability: task/benefit → captioned film player → purpose and first-use prompt → clearly labeled installation and source destinations → related capabilities with distinct jobs.

Film index: film artwork and titles with click-to-open controls. No autoplay. The individual film page includes transcript and short-cut destinations when verified.

## Design review before implementation

The first idea of thirty-three equal cards would read as a software directory. It is replaced by a personal introduction, a small amount of featured work and a searchable list. No KPI strip, invented testimonials, decorative node graph, anonymous stock imagery or placeholder overview player. Use one restrained blue interaction color, leave identity to the films, and avoid ornamental labels or numbered phases.

Static HTML, CSS and JavaScript. Content is built ahead of time from a public-only JSON catalogue. Progressive enhancement keeps all projects and links available without JavaScript. Reduced motion, visible focus, native media controls, captions, meaningful image alternatives and mobile layouts are part of the implementation.

## Revision after Michael’s feedback

Michael said the explicit “I’m Michael Jabbour” introduction and the link at the bottom felt too formal, and asked for the approach to move up a notch. The revision removes the repeated self-introduction, brings the already-developed “Good work has a next day” story into the hero, uses conversational task names, and replaces the formal closing/footer with a simple invitation. A small “Start anywhere” note and a gently arranged film board bring the work forward without inventing an identity or adding automatic motion. The baseline source and screenshots are retained locally for comparison. Capability names, actual functions, installation destinations and accessibility checks stay intact.
