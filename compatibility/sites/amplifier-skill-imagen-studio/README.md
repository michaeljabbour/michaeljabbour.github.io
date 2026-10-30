# Imagen Studio

Take the image from brief to chosen file.

Watch the [64-second film](https://michaeljabbour.github.io/amplifier-skill-imagen-studio/#film): an approved image, one request for a little brighter, and how the skill changes the image you chose instead of making a new one. The example in it is fictional.

A creative production skill for images and ASCII art. Clarify the brief, review concrete drafts and refine the file you actually chose, with the checks and delivery details needed to use it.

[Explore the site](https://michaeljabbour.github.io/amplifier-skill-imagen-studio/) · [Read the method](skills/imagen-studio/SKILL.md) · [Install guide](docs/INSTALL.md)

## What you get

- **Use the right amount of process.** Fast handles a clear small task; Guided resolves an ambiguity; Studio supports deliberate draft selection and refinement.
- **Preserve what you approved.** Anchor edits to the selected artifact and keep accepted and rejected branches traceable.
- **Receive a usable artifact pack.** Deliver the exact file with dimensions, alt text, literal text, lineage and an honest visual-review state.

## Install and try it

Requires Git and Python 3.11+. Run these commands from a terminal:

```sh
git clone https://github.com/michaeljabbour/amplifier-skill-imagen-studio.git
cd amplifier-skill-imagen-studio
python3 scripts/capability.py doctor
python3 scripts/capability.py install --dest ~/.agents/skills
```

The installer copies `skills/imagen-studio` as a complete folder into your chosen skills parent. Use the discovery path supported by your agent. It starts no service and configures no provider. Restart or refresh skill discovery in your host, then ask:

```text
Use Imagen Studio in Guided mode to prepare a fictional product-card illustration. It needs a 4:3 composition, room for a heading and no text inside the image. Draft the brief and acceptance checks first; show the provider and cost before any generation.
```

If your agent does not discover installed skills, point it directly at the complete folder and ask it to read `SKILL.md`. Reading the method needs no Python runtime. [Installation details](docs/INSTALL.md) cover conflict handling and optional native execution.

## How the work proceeds

1. **Direct the brief.** Name intended use, subject, dimensions, preserve constraints, references and acceptance criteria.
2. **Choose and refine.** Review actual drafts, select one and edit its accepted descendant instead of silently creating a replacement.
3. **Inspect and deliver.** Check the exact bytes and pixels when available, then deliver the file, preview and manifest.

## Example output

Fictional worked example. It illustrates the intended output; it is not a measured result or a real customer story.

```text
Fictional artifact plan: product card
Composition: 4:3; heading safe area reserved
Literal image text: none
Review: select one concrete draft before refinement
Delivery: chosen file, dimensions, alt text, parent hash
Current state: brief only; no image generated
```

## What is checked

Provider-free adapter lifecycle tests and a retained deterministic policy record cover the stated software and workflow boundaries. Image generation, pixels and user acceptance require their own actual review; the portable install performs no generation. See [validation](docs/VALIDATION.md) for the exact checks and limits.

## Retained implementation and references

[Native release guide](docs/NATIVE-README.md), [migration](docs/MIGRATION.md) and [validation](docs/VALIDATION.md) retain the original implementation and evidence boundaries. Provider execution uses an independently installed compatible MCP server; local ASCII conversion needs Pillow.

## Build the site

```sh
python3 scripts/capability.py build
python3 scripts/capability.py check
```

The static site includes a ZIP built from the canonical method, references and license. Runtime and provider setup remain separate from installing the portable method.
