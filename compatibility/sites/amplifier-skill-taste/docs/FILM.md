# The one-minute lesson

The film at the top of the site teaches the two questions before it mentions the skill. It runs 63.5 seconds and a 15-second cut is available.

## What it teaches

1. **See it before naming it.** Two yard-sale signs stand on the same fence. A car drives past both. The first sign is beautiful but says the wrong thing for a driver. The second says the right thing but nobody can read it at speed.
2. **Name the two questions.** Taste asks *does it belong?* (intentional choices, coherence, restraint). Elegance asks *does it work, effortlessly?* (simplicity, proportion, clarity). Each definition appears on the sign that is missing it.
3. **Place, then predict.** Both signs go on the map, upper left and lower right. The film asks which way each one should move, then holds two seconds of silence so the viewer can answer first.
4. **Move.** The first sign needs taste: say what drivers need. The second needs elegance: say less, bigger. They meet as one sign that still keeps the child's crayon sun.
5. **Check.** Can a driver read it in three seconds?
6. **Transfer.** The same two questions applied to an email, a slide, a room and an answer from an AI.
7. **Keep.** Three habits, then the skill as a partner that asks these questions with you, and the two questions on the final card.

The placements on the map are illustrative, not measured.

## How it was made

The film was made with the [Sizzle](https://michaeljabbour.github.io/amplifier-skill-sizzle/) skill. A storyboard with the script was reviewed and approved before any voice, music or picture was generated. An earlier draft that explained the skill's history instead of teaching the ideas was set aside at that review.

- **Narration:** ElevenLabs, one take per line chosen by measurement, each line leveled to -18 LUFS.
- **Score:** ElevenLabs music, edited on bar lines so the band enters on the first move and drops away for the habits.
- **Picture:** a deterministic HTML canvas, rendered frame by frame at 1920x1080 and 30 fps.

## What was checked

- Speech-to-text against the script: 99.6% word match. The recogniser dropped one "it".
- Layout audit on all 1,905 frames: no unexpected text collisions. The only overlaps are the faded signs leaving their places on the map, which is intended.
- Motion audit: no single-frame pops and no black frames.
- Loudness: -16 LUFS integrated with a true peak of -1.5 dBTP. The 15-second cut is -14 LUFS.
- An independent reviewer that had not seen the film being made reported ten findings. The ones about clarity were fixed before release:
  - both signs now sit on the map through the pause;
  - the car passes on "Nobody can read it";
  - the crayon sun is larger and hand-drawn;
  - the four transfer examples use plain words.

## Known limits

The three closing habits are all taste moves. The elegance move ("say less, bigger") appears in the lesson but not in the habits. Whether viewers retain the two questions has not been measured.
