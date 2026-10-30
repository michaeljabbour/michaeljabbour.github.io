# Market Fit

[Open the guide and get the skill](https://michaeljabbour.github.io/amplifier-skill-market-fit/).

A coaching skill that helps a person carve one clear, customer-named offer out of a large body of work, and grow their own judgment while doing it. It reads where the person starts, coaches through five bounded passes, stops on a fixed rule, and reports honestly on how both the work and the person moved. It does not hand anyone a finished positioning, and the AI does not become the judge of their product.

**The work** is the offer: a specific customer, the expensive problem they have, a name they would recognize, and evidence it lands. **The person** is the one carving it: whether they can explain the fit, defend it, and choose deliberately. Both climbs are jagged. The skill keeps the dips.

This project pairs the [`market-fit` skill](skills/market-fit/SKILL.md) and its [coaching reference](skills/market-fit/references/coaching.md) with an explanatory static website. The [benchmark plan](docs/BENCHMARK.md) sets the bar the skill has to clear; it has not been run yet.

## First use

Bring one product, project or body of work and your best guess at its customer. You leave with a fit card for the offer and a separate growth card for your judgment.

```sh
git clone https://github.com/michaeljabbour/amplifier-skill-market-fit.git
cd amplifier-skill-market-fit
python3 scripts/capability.py install --dest ~/.agents/skills
```

Requires Git and Python 3.11+. Use the skills directory supported by your agent. Ask for Market Fit in a new session and supply one real task. The [install guide](docs/INSTALL.md) explains the complete ZIP alternative and safe updates.

## Use the skill

Give an agent the skill and the body of work: a repo, a deck, a site, or a paragraph. Say who you think it is for. The agent opens with a few plain questions, agrees a target with you, and then works attempt-first: you try each pass, it responds, and you choose. Expect short turns, one question at a time, and the occasional dry joke.

If your tool supports reusable skills, copy the `skills/market-fit/` directory (`SKILL.md` plus `references/coaching.md`) according to that tool's instructions. Keep the relative `references/` path intact.

### In Amplifier

This repository is also an Amplifier bundle (`market-fit`). Add its behavior to your current host:

```bash
amplifier bundle add "git+https://github.com/michaeljabbour/amplifier-skill-market-fit@main#subdirectory=behaviors/market-fit.yaml" --app
```

For a local checkout that stays in step with your edits, use `file:///<path-to-checkout>/behaviors/market-fit.yaml` instead. Remove with `amplifier bundle remove market-fit-behavior --app`. Start a new session, then:

- **Skill:** `/market-fit`, or ask for it by name. Nothing loads until it is used.
- **Mode:** `/fit` sets a coaching posture for the session: your attempt first, one question per turn, every file edit asks you first. `/mode off` leaves it.
- **Recipe:** `@market-fit:recipes/market-fit-round.yaml` runs one bounded round that pauses for your answers at each gate, then writes a fit card and a growth card to `.market-fit/` in your working directory. It never edits your work.

The skill is registered through `tool-skills`. If no other bundle in your host configures skill sources, Amplifier stops scanning its default skill directories (`.amplifier/skills` in the workspace and `~/.amplifier/skills`); add them to your own skills configuration if you need them. Don't also keep a hand-copied `market-fit` in `~/.amplifier/skills`, or two copies will compete.

Example requests:

> Use market-fit on this repo. I think it's for research labs, but nobody outside our group uses it. Target: a lab manager understands it from the README's first paragraph.

> Use market-fit to help me rename this internal tool for an outside audience. Coach me, don't name it for me. Three rounds at most.

> We've pitched this three times and people nod and do nothing. Use market-fit to find out why, and show me where my own reasoning is weakest.

A useful run ends with two cards. See [a worked example](docs/EXAMPLES.md), dips included.

## How it works

1. **Opening read.** Three to five plain questions. The agent quotes your answers and privately places you on five dimensions: Customer, Problem, Naming, Reasoning, Evidence.
2. **Five passes.** Find the expensive problem. Name it for the customer. Show it in one picture. Teach the why. Test against the target. Each pass pairs a teaching move with a gate.
3. **You choose.** Every choice is logged with the option you turned down and your reason. No reason, no entry.
4. **Two cards.** A fit card for the work and a growth card for you, with the full trace from start to finish.

## The film

A 53-second film explains the idea: an AI coach that sharpens your pitch and you, round by round, until the work reaches the launch zone. It plays on the [site](https://michaeljabbour.github.io/amplifier-skill-market-fit/#film) and lives at `site/assets/market-fit-film.mp4` with English captions. The example in it is fictional.

## How it stops

The target is agreed before the first pass. By default it is the launch zone: the fit card is clear enough to put in front of strangers in a campaign (one customer, a costed problem, a name a stranger can decode, a ten-second picture, a user who can defend every line, and a real signal or a plan to get one). The run stops there. Three rounds at most. A failed gate sends you back to that pass only, never through all five again. If a full round doesn't move the work, the problem is upstream (the wrong customer or the wrong pain), and the skill says so and stops. Every run ends with both cards, including runs that miss.

## Local development

The site follows the family's small Python static-builder approach: HTML, CSS, and JavaScript with no backend or runtime dependencies. Use Python 3.11 or later; no package installation is required.

From the project directory:

```sh
python3 scripts/build.py
python3 scripts/check.py
node --check site/site.js   # optional JavaScript syntax check; needs Node.js
python3 -m http.server 8000 --bind 127.0.0.1 --directory _site
```

Open <http://127.0.0.1:8000> in your browser. Stop the server with `Ctrl+C`. Re-run the build after source changes. `_site/` is generated output.

The build reads the opening questions, dimensions, teaching moves, and diagnosis rows straight from the coaching reference, and the benchmark rows from `docs/BENCHMARK.md`, so the page never forks the method. The check verifies local links and fragments, that the page and downloads match the canonical skill byte for byte, and the ZIP contents. See [site details](site/README.md).

The Pages workflow builds and checks `_site/` on pushes to `main`, then publishes only that static output. It uses GitHub's official actions pinned to fixed commits and needs no project secrets.

## Project contents

- `skills/market-fit/SKILL.md`: the method.
- `skills/market-fit/references/coaching.md`: opening questions, five dimensions, teaching moves, diagnosis table, card templates, and voice examples.
- `bundle.md`, `behaviors/market-fit.yaml`: the Amplifier bundle and its installable behavior.
- `modes/fit.md`: the `/fit` mode.
- `recipes/market-fit-round.yaml`: one staged, human-gated round.
- `docs/EXAMPLES.md`: a fictional worked run with both cards.
- `docs/BENCHMARK.md`: the tests the skill has to pass. Not yet run.
- `scripts/build.py`, `scripts/check.py`: dependency-free build and integrity checks.
- `site/`: page template, metadata, styles, local assets, and interaction code.
- `_site/`: generated website and downloadable skill assets.

## Limits

This is a structured coaching aid, not a market research method, a validated assessment, or a substitute for talking to customers. Dimension placements describe one person on one piece of work on one day; two careful coaches may disagree, and none of it measures talent. A fit card is a hypothesis until a real customer signal supports it. The examples on the site and in the docs are invented.

## License and provenance

MIT; see [LICENSE](LICENSE). The family theme snapshot keeps its own [MIT notice](site/theme/LICENSE). The page follows the Amplifier Smart Tools family site as a design and implementation reference.


## Portable capability and ownership

Turn the work into one clear offer, and learn to defend it.

Read the [installation guide](docs/INSTALL.md) for the supported local path and [consolidation record](docs/CONSOLIDATION.md) for ownership and evidence limits. Canonical catalog name: **Market Fit**; repository: `amplifier-skill-market-fit`.
