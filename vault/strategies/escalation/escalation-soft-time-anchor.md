---
id: escalation-soft-time-anchor
phase: escalation
status: active
created: 2026-04-01
incompatible_goals: [extended-window, decline-gracefully, just-being-polite]
goal_stats:
  quick-meet-window: { used: 0, used_well: 0 }
  flexible-short-window: { used: 0, used_well: 0 }
---

## What it is

**Targets:** escalation 40 → 70. Bridges to specific-invite. Requires
rapport ≥ 60 — soft anchors land best on threads that are warm but
ambiguous on whether the meet is yet "assumed."

**Mechanisms:** A7 scarcity (real options, soft) + A17 calibrated
"no as safety" + A16 autonomy via window not deadline + H1 mixed
signals (clear interest + soft commitment) + A11 self-perception via
counter-proposal.

The move suggests a meet by anchoring on a *window* without demanding
a specific commitment. "I'm around thursday-ish if you want to grab a
drink" rather than "thursday at 8?" The softness is the mechanism: a
day-window installs A7 scarcity (he is not endlessly available — the
window has edges) while preserving A16 autonomy (she shapes the
specifics if she wants the meet) and A17 no-as-safety (declining a
window costs her nothing — there's no specific time-and-place she's
rejecting).

The move is calibrated for ambiguous-warmth threads — ones where the
specific-invite would be the next obvious move but the read on her
exact warmth level is uncertain. The soft anchor is a probe that
extracts more signal than the specific invite would. Her response
classifies her: a counter-proposal of a specific time is a strong
IOI (I5) and an A11 self-perception lock-in (she just took agency on
*when*, which she'd only do if she wanted it); a soft "yeah maybe
that could work" is a tepid IOI that suggests another rapport rung
before specific-invite; a deflection without counter is signal to
hold position.

H1 mixed signals do quiet work here: the move says clearly "I want
to meet you" while signaling softly "and I'm not pressed about it."
That contradiction is the hook her mind tries to resolve, and the
resolution she reaches via her own counter-proposal is hers — A11
sticks better than a yes to an explicit ask.

The soft-anchor is a *bridge*, not a destination. Once she counter-
proposes or warms further, graduate to `escalation-specific-invite`
within 1-2 turns. Sitting on the soft anchor turn after turn is
how the thread dies of comfort.

Example illustrations (window-shaped, not point-shaped):

- "i'm around thursday-ish if you want to grab a drink."
- "this week's mostly open after wednesday. drinks somewhere?"
- "weekend-ish if you're up for the wine bar conversation we keep
  half-having."
- "thursday or friday i could be talked into the place you mentioned."

Each names a window with edges (real scarcity, not infinite
availability), invites her to specify, and stops.

## When it works

- Rapport ≥ 60, with at least one warm reciprocation that signals
  she's open to escalation but hasn't future-paced explicitly. The
  H1 mixed-signal mechanism needs warmth to register as confidence-
  with-options rather than as hedging from low interest.
- `days_remaining > 4`. With more time on the table, the window-
  shape is honest scarcity; with less, the soft anchor reads as
  evasion of the harder ask the timeline actually demands.
- She's not a hard planner-type. Planner-archetypes (matches whose
  prior messages cite specific times, schedules, who-asks-when)
  read soft anchors as flake-coded. For those matches go straight
  to `escalation-specific-invite`.
- The window has real edges. "I'm around thursday-ish" works; "I'm
  around whenever, let me know" collapses A7 entirely and inverts
  to endless-availability.

## When it fails

- **Window too wide → A7 collapse.** "Whenever works" or "any time
  this week" removes the scarcity edge entirely. The mechanism
  requires the window to feel finite; infinite windows signal he has
  no other call on his time, which downstream-encodes as low MV via
  A19.
- **Used inside a tight timer → A7 inversion.** With `days_remaining
  < 3`, soft anchors signal he doesn't grasp the actual constraint.
  A goal_type of quick-meet-window with the meet 48 hours out needs
  `escalation-specific-invite` or `escalation-direct-ask` — the
  softness reads as ambivalence, not generosity.
- **Sat on across multiple turns → H1 mechanism failure +
  A14 desire-gap closure via stagnation.** If she counter-proposes
  or warms and he doesn't graduate to specific within 1-2 turns,
  the soft anchor stops reading as soft-confidence and starts
  reading as inability-to-close. Death by comfort.
- **Stacked hedges → A1 frame collapse.** "If you're free thursday-
  ish maybe?" stacks two softeners — the window itself is the
  softener, no further hedging needed. Additional hedges signal
  permission-seeking and inverts A16.
- **Planner-match misread → autonomy mismatch.** A planner whose
  bio and prior messages broadcast "I plan things" reads window-
  shaped invites as flake-coded. The autonomy she values is the
  autonomy of *picking from concrete options*, not the autonomy of
  filling in a vague window. Wrong calibration kills the move.

## Outcomes by goal

### quick-meet-window

<!-- (no records yet) -->

### flexible-short-window

<!-- (no records yet) -->

---

## Pending observations

<!-- Agent appends here. On threshold (3 entries about a single pattern)
     the agent integrates above and clears the pattern from this list. -->
