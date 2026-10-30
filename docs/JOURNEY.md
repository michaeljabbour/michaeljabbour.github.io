# Navigate through the work

The portfolio story follows a person trying to make something another person can understand, use and continue. The journey gives that story a practical navigation structure. Each moment starts with a human question, names something to work toward and shows the capabilities that can help.

`content/journey.json` is the source for this sequence and its framing. `content/portfolio.json` remains the source for the individual capabilities, their category membership, descriptions and destinations. The journey adds context without merging capabilities or turning every project into a mandatory seven-step process.

## Order and complete coverage

| Position | Category ID | Moment | Capabilities with this primary home |
| --- | --- | --- | --- |
| 1 | `understand` | Figure it out | Unknowns, Research, Long Read, Knowledge, Cognitive Simulation |
| 2 | `choose` | Make a call | Market Fit, Decisioncraft, Right Shape, Intent to Plan |
| 3 | `build` | Build something | Build with Amplifier, Build with Tauri, Build with Torque, Constraint Builder, Forge, Desktop Tasks |
| 4 | `improve` | Make it better | UX Ergonomics, Taste × Elegance, Worth Using, Preceptor, Session Doctor, Fast Decisions |
| 5 | `create` | Make it visible | Imagen Studio, Imagen Provider, Sizzle, TeaserKit |
| 6 | `adapt` | Take it somewhere new | Migrate, Transfer, Pipeline |
| 7 | `continue` | Pick it up again | Amplifier Data, Memory, Project Handoff, Good Teammate, Team Access |

All 33 public capabilities keep one primary home. The order puts making the work visible before taking it into a new setting; keeping the record and leaving a next step closes the story. “Take it somewhere new” means a move of language, host or release workflow. It is distinct from telling the story or showing the product.

The `lead_ids` offer a few concrete places to begin within each moment. They are a small selection from that category, not a ranking, a dependency list or permission to hide the remaining tools. The full category should remain reachable.

## How the navigation should behave

- Let someone choose the moment that matches their situation, with a visible selected state and the same order wherever the journey appears.
- Show the human question, expected output and relevant tools together. A category title alone is too little context for someone arriving cold.
- Let someone move forward, go back or jump to another moment. Keep an all-capabilities path for people who already know what they want.
- Use the reflections to make feedback and revisiting a direction part of the work. An ordered story can coexist with an iterative practice.
- A route or shared URL should restore the chosen moment. Keyboard controls, visible labels and reduced motion should work without requiring the film to play.
- Keep the tools distinct. In particular, Data stores exact evidence, Memory retrieves project records, and Handoff explains the current state independently of Memory.

## Relationship to the film

The supplied overview captions are the evidence for the six narrated moments:

| Moment | Narration starts |
| --- | --- |
| Figure it out | 28.87 seconds |
| Make a call | 34.86 seconds |
| Build something | 40.61 seconds |
| Make it better | 46.88 seconds |
| Make it visible | 51.08 seconds |
| Pick it up again | 58.44 seconds |

“Take it somewhere new” has no distinct narrated beat in the supplied captions. Its `film_start` is deliberately `null`; the site must not invent a matching film timestamp or imply that this timing corrects the end-card animation. These values can support optional jumps to the actual narrated moments. They do not require automatic playback or a time-driven change to the visitor’s selected task.


## Scope of the language

The journey is inspired by a human-centered way of working: understand someone’s situation, make choices, put a version in front of them, learn and continue. It is not a claim of certification, a named institutional methodology or a completed user study. The outputs are targets for a visitor’s work, not reported results. Cognitive Simulation remains hypothesis exploration rather than evidence from participants; the different building guides remain alternatives for different applications.
