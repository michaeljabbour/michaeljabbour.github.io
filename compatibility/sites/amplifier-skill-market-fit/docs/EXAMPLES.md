# A worked run, start to finish

This is an **invented example**. The lab, the people, the product, and every number are fictional. No customer research occurred and no test was run. It shows the shape of a run, including the parts that go badly.

## The work

A university lab has built an open-source library for matching patient records across hospital datasets. It does fuzzy matching, graph-based entity resolution, audit logs, a command-line tool, and a notebook plugin. The lab calls it LinkGraph. Two years in, a handful of labs use it and nobody else has noticed.

The user is the lab's research engineer. Target, agreed at the start: *a research coordinator can say what it does after one read of the landing page.* Budget: three rounds.

## Opening read

> **Coach:** Who uses this first? Describe their worst Tuesday.
>
> **User:** Data scientists in health research. Their worst Tuesday is when the join keys don't line up.
>
> **Coach:** One sentence for a slide. Go.
>
> **User:** "LinkGraph is a scalable, graph-based entity resolution toolkit for biomedical data."

Private placement, with evidence: Customer **Early** ("data scientists" is a category, not a person). Problem **Early** (describes the mechanism). Naming **Early** (likes the name, can't say why). Reasoning **Developing** (can explain why graph matching beats exact matching). Evidence **Early** ("a few labs use it").

## Round one

**Find.** The coach models a pain sentence first, then asks the user to write theirs.

> **User:** "Researchers waste time cleaning data."
>
> **Coach:** That's true of every researcher alive, which is the problem. Who, which data, and what does it cost them?
>
> **User:** "A coordinator merging three hospitals' records before a grant report spends weeks hand-matching patients, and still double-counts some."

Gate: role, job, cost. **Pass**. The user chose this sentence over "data scientists lose hours on joins" because "coordinators are the ones who get blamed when the count is wrong."

**Name.** Three candidates: LinkGraph, OneRecord, CleanCohort. The user predicts strangers will guess LinkGraph is "a graph database." Gate: **pass** for OneRecord. The user chose OneRecord over CleanCohort because "cohort is a word only epidemiologists love."

**Show.** The user's first sketch has five boxes and a pipeline. The coach points at the leftover stone. Second try: *before: three spreadsheets, a highlighter, a nervous email to the PI; after: one list, each patient once, a log of every merge.* Gate: **pass**.

**Teach.** The coach plays skeptic: "Why wouldn't the hospital's IT team just do this?" The user can't answer, then guesses "they're busy." Gate: **fail**. Naming also drops to **Early**: the user now doubts OneRecord, because "if IT owns it, maybe the name should talk to IT." Dip labeled: *standards rose faster than the draft*.

**Test.** User confidence before scoring: high. Result against the target: a mock coordinator reading the draft page still asks whether it needs IT approval. **Miss**. Diagnosis row: *the user can't answer pushback → return to Teach.* Reasoning drops to **Developing** after a brief high: dip labeled *first miss shook a confident answer*.

## Round two (Teach and Test only)

The user leads; the coach prompts only at the gates. The user names the riskiest assumption without help: *coordinators can't install software without IT sign-off.* They decide the page should lead with "runs in your browser, nothing to install," and keep OneRecord because "the coordinator is still the one who feels the pain; IT just needs a line." Test: target **met** in the mock read. Confidence before scoring: medium, which matched.

## The two cards

```
FIT CARD · OneRecord · round 2 of 3
Customer          A research coordinator merging three hospitals' data before a grant report
Expensive problem The same patient appears under different spellings and IDs, so counts are wrong
Cost today        Weeks of hand-matching per report (user's estimate; unverified)
Name + promise    OneRecord · Merge your sites and trust the patient count
Picture           Three spreadsheets and a highlighter → one list, each patient once, every merge logged
Why it holds      Coordinators carry the blame for wrong counts · Riskiest assumption: they can run it without IT approval
Evidence          Target: understood in one read · Result: met in a mock read · Signal: none from real coordinators yet
```

```
GROWTH CARD · research engineer · fictional
Started at   "A scalable, graph-based entity resolution toolkit for biomedical data."
             Customer E · Problem E · Naming E · Reasoning D · Evidence E
Got to       "Merge your sites and trust the patient count."
             Customer S · Problem S · Naming D · Reasoning S · Evidence D
Trace        Naming rose at Name, fell at Teach (standards rose faster than the draft), recovered in round two.
             Reasoning peaked at Teach, fell at the first Test (a confident answer met a miss), then rose higher.
Decisions    Find · coordinator over data scientist · "they get blamed when the count is wrong"
             Name · OneRecord over CleanCohort · "cohort is a word only epidemiologists love"
             Teach · lead with "nothing to install" · "IT just needs a line"
Calibration  Test 1: said high, missed · Test 2: said medium, met
Next time    Start on Evidence, scaffold level "together". Talk to three real coordinators first.
```

Not every dimension ended Strong, and Evidence stayed thin because there is still no real customer signal. The card says so. That is the useful part.
