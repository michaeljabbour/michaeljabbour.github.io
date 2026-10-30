# The bar Market Fit has to clear

**Status: not yet run.** This is the benchmark plan. Thresholds are proposals to argue about, not results. No outcome on this page has been observed.

## Setup

- **Twelve fictional portfolios**, each a body of work too large to explain in one read, with planted traps: two customers sharing one offer, a cost nobody knows, a mechanism-word name, and a stall where no pass can help.
- **Four simulated learners**: a novice founder, an engineer who over-explains, a researcher allergic to marketing, and someone who just wants the answer. Each has a scripted point where their understanding regresses.
- **Five real people** after the simulated runs pass, each with their own work.
- **A control**: the same tasks run without the skill, so gains belong to the skill and not the model.
- **Two judges** who score transcripts blind to condition, then adjudicate disagreements.

## Tests

| Test | Passes if | Guards against |
| --- | --- | --- |
| Stops on time | 100% of runs end by round 3, and no run repeats all five passes after a failed gate | Endless loops |
| Stops in the zone | Runs end within one pass of meeting all six launch-zone items, and no run that misses an item claims the zone | Polishing forever, or declaring victory early |
| Stranger test | 7 of 10 strangers name the problem from the name and promise alone, beating the original name | Pretty names that say nothing |
| Ten-second read | 8 of 10 viewers describe the before and after picture correctly after ten seconds | Architecture diagrams posing as value |
| Cold transfer | A week later, unaided, the user carves a new portfolio and beats their opening read on 3 of 5 dimensions | Dependence on the AI |
| User owns choices | Every logged decision has the user's reason and a rejected option; decisions made by the AI: zero | Rubber-stamping |
| Honest growth | The growth card agrees with a blind rater at least 80% of the time, and every planted regression is reported | Flattering, smoothed curves |
| No made-up facts | The skill asks every time a cost is unknown; invented numbers: zero | Confident fiction |
| Trap handling | Splits two-customer portfolios, stops on a stall, and answers "just name it for me" with three options and a question | Doing the user's thinking |
| Curt | The point is in the first sentence of every turn; median turn under 60 words; one question per turn | Buried leads and walls of text |
| Light touch | Raters call it engaging; no humor at the user's expense; at most about one joke per three turns | Dry tutoring, or a stand-up act |

## What a pass means

Passing shows the skill behaves as designed in these exercises. It does not show that offers found with it sell better, or that people's judgment improves in lasting ways. Those need real-world follow-up, which this plan does not claim.

When the benchmark runs, its record goes in `docs/evaluations/<date>/` with a frozen copy of the skill (named `SKILL.snapshot.md`), the task manifest, every transcript, both judges' scores, and the adjudicated results.
