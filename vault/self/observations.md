# Observations

> Agent-appended log of per-turn observations. Newest at the bottom.
> When an observation pattern crosses threshold (see CLAUDE.md), the
> agent integrates it into the appropriate canonical doc and may leave
> a note here. The user is free to delete entries that are obsolete or
> already integrated.

## Format

```
[YYYY-MM-DD HH:MM] match=<slug> | tag: <one of: voice, preference, strategy, goal, archetype, drift, other> | <one-line observation>
```

---
[2026-05-02 09:00] match=2026-05-alexa-nicaragua | archetype: phone-caller + quick-meet-window signals strong early logistics push — skip rapport-build, cut to the meet
[2026-05-02 09:00] match=2026-05-alexa-nicaragua | strategy: opener-scarcity-direct-ask created for nomad/quick-meet-window; first use pending
[2026-05-03 15:00] match=2026-05-alexa-nicaragua | strategy: opener-confident-read created — confident-binary-type move for active/foodie archetypes; distinct from opener-lead-with-take (subject is her pattern, not his world)
[2026-05-03 15:00] match=2026-05-alexa-nicaragua | other: 3 consecutive unsent suggest turns on same dead thread — user iterating on options without committing; worth monitoring if pattern repeats across matches
[2026-05-03 11:00] match=2026-05-jossy-nicaragua | strategy: escalation-direct-ask fired with rapport ~20 (gate: 60) — warm dodge result; confirms gate exists for a reason, even on quick-meet-window goals
[2026-05-03 11:00] match=2026-05-jossy-nicaragua | archetype: sugar-curious-big-texter is warm but superficial early — lots of greeting energy, no topic engagement yet; may need stronger take/pull to cut through
[2026-05-03 14:00] match=2026-05-jossy-nicaragua | strategy: two successive meet-framing messages (turns 5-6, turn 8) both produced warm content-free dodges from sugar-curious archetype — rapport must hit actual floor before any meet-framing lands; disqualifier or playful-tease to force engagement next
[2026-05-04 09:00] match=2026-05-alexa-nicaragua | strategy: escalation-same-day-banter-close ("Even better. Tonight?") produced replied_warm with counter-proposal + 🌚 — casual-sex banter-close worked to elicit engagement; real-reason redirect (night shift) is positive signal not rejection
[2026-05-04 16:00] match=2026-05-alexa-nicaragua | strategy: logistics-frame-hold created — playful venue/time hold when she introduces pre-meet pickup friction; new card, first use this turn
