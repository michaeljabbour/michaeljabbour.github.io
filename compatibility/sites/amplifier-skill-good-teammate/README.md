# Good Teammate

Get the right help. Keep the meaning intact.

Watch the [67-second film](https://michaeljabbour.github.io/amplifier-skill-good-teammate/#film): a careful "not tested" that turns into a billboard, and how the skill keeps the fine print attached. The example in it is fictional.

A coordination skill for shared work. Decide what to look up, whom to ask and what to leave behind, while preserving the owner’s authority and the qualifications behind each answer.

[Explore the site](https://michaeljabbour.github.io/amplifier-skill-good-teammate/) · [Read the method](skills/good-teammate/SKILL.md) · [Install guide](docs/INSTALL.md)

## What you get

- **Ask a question that changes the work.** Route facts to retrieval, interpretation to expertise and preferences to the accountable owner.
- **Prevent quiet misunderstandings.** Carry “not tested,” “proposed” and other material qualifications into handoffs and summaries.
- **Make contributions usable.** Name the approved inputs, permitted actions, expected evidence and current state instead of treating delivery as completion.

## Install and try it

Requires Git and Python 3.11+. Run these commands from a terminal:

```sh
git clone https://github.com/michaeljabbour/amplifier-skill-good-teammate.git
cd amplifier-skill-good-teammate
python3 scripts/capability.py doctor
python3 scripts/capability.py install --dest ~/.agents/skills
```

The installer copies `skills/good-teammate` as a complete folder into your chosen skills parent. Use the discovery path supported by your agent. It starts no service and configures no provider. Restart or refresh skill discovery in your host, then ask:

```text
Use Good Teammate to draft a local request for a specialist review. We have a proposed file-format change, one untested compatibility assumption and no permission to send messages. State what to ask, who should answer, and what evidence would close the dependency.
```

If your agent does not discover installed skills, point it directly at the complete folder and ask it to read `SKILL.md`. Reading the method needs no Python runtime. [Installation details](docs/INSTALL.md) cover conflict handling and optional native execution.

## How the work proceeds

1. **Find the missing piece.** Distinguish an existing fact, specialist judgment, owner preference or authorized contribution.
2. **Coordinate a bounded request.** Draft one useful question or update with exact inputs, authority and expected evidence.
3. **Preserve the current record.** Keep attribution, limitations and additive corrections so the next person knows what they can rely on.

## Example output

Fictional worked example. It illustrates the intended output; it is not a measured result or a real customer story.

```text
Fictional contribution request
Need: verify format-B compatibility
Input: exact proposed revision and fixture
Allowed action: local read-only review
Qualification: support is suspected, not tested
State: drafted; not sent; no acceptance yet
Close when: reproducible compatibility result is returned
```

## What is checked

693 native host unit tests and isolated bundle validation passed; portable packaging is checked separately. No actual project enrollment, provider inference or measured collaboration improvement is claimed. See [validation](docs/VALIDATION.md) for the exact checks and limits.

## Retained implementation and references

[Migration map](docs/MIGRATION.md) records the original source paths and current roles. Primary Git history, native engines, tests, examples, and evaluation assets remain in this checkout. [Native guide](docs/NATIVE-README.md) preserves the original project documentation; old install URLs and runtime claims there are historical and need current verification. [Validation](docs/VALIDATION.md) records actual checks and limits.

[Optional adapters and retained owners](docs/OPTIONAL-ADAPTERS.md) maps the separate Collaboration bundle, posting utilities and M365/Slack/Google provider code. They retain their existing infrastructure homes. The five protocol references included here do not replace those native workflows, and the portable method requires none of them.

## Build the site

```sh
python3 scripts/capability.py build
python3 scripts/capability.py check
```

The static site includes a ZIP built from the canonical method, references and license. Runtime and provider setup remain separate from installing the portable method.

## Repository migration

This repository was renamed from `amplifier-skill-good-teammate` to `amplifier-capability-good-teammate`. Existing installed method names, bundle aliases and native interfaces stay the same. See the [migration guide](https://michaeljabbour.github.io/migration/) and [repository map](https://michaeljabbour.github.io/migration/mapping.json) for source URL updates.
