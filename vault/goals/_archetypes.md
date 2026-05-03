# Goal archetypes

Enumerated set of goal types. Strategy cards declare compatibility
against these ids. Match files set exactly one `goal_type` from this
list.

Each archetype names the **dominant psychological dynamics** the
timeline forces — which mechanisms (see `_psychology.md`) get re-
weighted up or down. Strategy selection and phase-progress allocation
flow from these.

Add new ids sparingly — proliferation defeats the point.

---

## quick-meet-window

Drinks within the current trip / week. Casual, no pretense of long-
term. Compresses rapport. Pushes logistics earlier.

**Dominant mechanisms.** Scarcity (A7) as the framing layer
everything else hangs off — real time-bounded windows, not
manufactured urgency. Commitment momentum (A3) compressed: rapport →
escalation in fewer turns than default. Pre-suasion (A1) doing extra
work because there's less recovery time from a weak opener.

**Phase-progress allocation.** Spend less on rapport — target
~50-60, not 80. Push qualifying and escalation in parallel rather
than sequentially. Logistics ask comes around message 5-7 in a warm
thread, not 9-12.

**Phase scoring (under this goal).** Lower bars on rapport/qualifying
(push fast), higher bars on escalation/logistics (need clear signal
before counting as "solid").

- rapport: 60 = any substantive non-pleasantry reply that matches
  energy. 100 = one volunteered specific + asked back.
- qualifying: 60 = one stated preference or take. 100 = mutual
  texture across a couple turns.
- escalation: 60 = she future-paced OR volunteered availability.
  100 = explicit "we should" or near-yes.
- logistics: 60 = a day named (her or his). 100 = day AND place.
- (opener / confirm: baseline rubric.)

**What kills it.** Ambiguity. "Maybe sometime this week" doesn't fit
the timeline; signals you don't actually have a constraint, which
makes urgency feel manufactured. Long rapport drift past day 2-3 of
a 7-day window collapses momentum.

## flexible-short-window

Same physical window as quick-meet, no push. Meet if it clicks. The
default for most matches in the current city.

**Dominant mechanisms.** Liking (A6) + commitment ladder (A3) +
light Zeigarnik (A15). Standard rapport-into-logistics arc.

**Phase-progress allocation.** Build real rapport (60-80) before
qualifying. Don't compress unless signals are unusually hot.
Logistics around message 7-11.

**Phase scoring (under this goal).** Standard / baseline. No
overrides — use the universal rubric in
`prompts/orchestrator.md` as-is.

**What kills it.** Letting it drift past 2 weeks. Match-decay is
real — the longer between match and meet, the lower the meet
probability. After ~10 days the thread is going cold regardless of
how it feels in the moment.

## extended-window

Both local, willing to invest more time across messages. Still
casual; not LTR. Appropriate when neither party is on a hard timer.

**Dominant mechanisms.** Zeigarnik (A15) + variable-ratio
reinforcement (A13) + otherness (A14). Without the meet as natural
close, the thread sustains its own tension. Channel-jumps (voice
note, call, photo from your day) do work text alone can't.

**Phase-progress allocation.** Rapport can run high (80+) for many
turns. Open loops compound — "when we finally do this in person"
becomes recurring frame. One concrete plan-anchor on the horizon
("I'm out there in three weeks") changes everything; without it the
thread has no telos and dies of comfort.

**Phase scoring (under this goal).** Higher bars on rapport /
qualifying (need real depth before counting as solid); slightly
lower bar on escalation (casual future-pacing is enough — no need
to manufacture intensity).

- rapport: 60 = she's volunteered something personal AND topic has
  genuine texture. 100 = consistent show-up across days, depth.
- qualifying: 60 = mutual taste signals exchanged. 100 = real values
  / preference alignment surfaced.
- escalation: 60 = casual future-pacing from her. 100 = a real
  plan-anchor on the horizon.
- logistics: 60 = a day floated. 100 = day AND place agreed.
- (opener / confirm: baseline rubric.)

**What kills it.** Daily good-morning texts (otherness collapse).
The relationship pretending to be in a phase it's not. Closing the
desire-gap before any proximity. Treating extended-window as
"infinite-window" — the meet still has to happen or the thread
metabolizes into pen-pal-zone.

## just-being-polite

Not pursuing, but not ghosting either. Low-frequency replies, no
investment. Used when interest has dropped but a hard close isn't
warranted.

**Dominant mechanisms.** Variable-ratio (A13) at low frequency.
Holding pattern.

**Phase-progress allocation.** No active progression. Reply rate
roughly matches hers; no escalation moves; no logistics pushes.

**Phase scoring (under this goal).** Phase progress is frozen — do
not advance scores beyond their values when this goal was set. The
goal explicitly suspends progression; re-scoring upward implies
pursuit that contradicts the goal.

**What kills it.** Re-pursuing when nothing has changed. If interest
returns, switch goal_type explicitly — don't drift back.

## decline-gracefully

Actively winding down. Polite, brief, no door left open. Used when
goals have diverged and continuing would mislead.

**Dominant mechanisms.** Autonomy (A16) + sociometer (A10). All
persuasion off the table. Acknowledge cleanly, don't argue.

**Phase-progress allocation.** Reverse — no axis is being raised.
The exit itself is the move. Sociometer-positive disengagement: she
sees he can be told no without flinching, and the move doesn't burn
the bridge in case anything changes later.

**Phase scoring (under this goal).** Phase progress is being
intentionally let down. No upward scoring; expect rapport /
escalation / logistics to decay turn-over-turn as the thread
gracefully closes.

**What kills it.** Trying to reverse the decline. "But what if we
just…". Sulky one-word replies. Re-pitching after she's said no.
Apologetic withdrawals that re-pursue under the cover of closure.

## reconnect-later

She's leaving / I'm leaving and there's a real possibility of overlap
in a future city. Keep the door open without active pursuit.

**Dominant mechanisms.** Zeigarnik (A15) + scarcity-as-time (A7) +
pre-suasion reset (A1). The reopener is a fresh first impression.

**Phase-progress allocation.** Reset to opener-low. Don't reference
the old thread's stuckness. Don't apologize for the gap. Anchor on
something present-tense — "just walked past that bar you mentioned,
can confirm it's still hostile to humans." If she re-engages, the
thread proceeds normally and you re-allocate per current overlap
window.

**Phase scoring (under this goal).** Reset all axes to low (opener
≤ 30, all later phases 0) regardless of where they previously sat —
the long gap broke the substrate; treat the next message as a fresh
first impression.

**What kills it.** "Hey stranger." "Long time no talk." "Sorry I
disappeared." All sociometer leaks (A10) — they put her in
evaluator-frame and reset the gauge low.

## platonic-curiosity

Match is interesting as a person but romantic interest has faded
from one or both sides. Optional; only adopt if she's surfaced it
explicitly.

**Dominant mechanisms.** Out of scope for tactical optimization.
Drop pursuit moves. Standard friendly-acquaintance dynamics.

**Phase-progress allocation.** Not applicable — escalation/logistics
axes don't progress under this archetype.

**Phase scoring (under this goal).** Escalation, logistics, and
confirm are frozen at 0 by definition — the goal explicitly
forecloses pursuit. Opener and rapport scores are read against the
baseline rubric but inform conversation, not advancement.

## casual-sex

Extremely flirty, sexually suggestive approach targeting a same-day
or very-short-window physical meetup. No rapport arc. No pretense of
a longer timeline.

**Dominant mechanisms.** Scarcity (A7) at maximum compression —
same-day or nothing. Pre-suasion (A1) is critical: the register must
be set in the first real message so there's no bait-and-switch later.
Misattribution of arousal (A11) — move fast enough that her
excitement attaches to you, not just the situation. Reactance (A9)
— invite, don't push; let her opt in, don't recruit.

**Phase-progress allocation.** Opener and minimal rapport must land,
then skip straight to escalation and logistics. Rapport target: 30-40
(enough warmth not to read cold or threatening). Qualifying: scan
only for hard red flags (relationship-pusher, obviously wrong vibe).
Push escalation and logistics in the same message or back-to-back
turns. No multi-day arc.

**Phase scoring (under this goal).** Compress everything. Rapport and
qualifying bars are low; escalation and logistics bars are high (need
clear yes before counting as solid).

- opener: 60 = she replied with any substance or matched flirty energy.
  100 = she escalated or set the tempo above yours.
- rapport: 40 = she's engaged and not cold. 60 = warm and
  reciprocating. 100 = explicit receptiveness signal.
- qualifying: 30 = no hard red flags. 60 = hinting at openness to
  something casual.
- escalation: 60 = she matched the flirty/suggestive register.
  100 = explicit or near-explicit yes to meeting today.
- logistics: 60 = today named. 100 = specific time AND place today
  confirmed.
- (confirm: baseline rubric.)

**What kills it.** A platonic-register opener that then pivots to
sexual — that reads as bait-and-switch and loses her. Over-texting
before the ask (momentum dies). Treating her profile cues as rapport
material. Any message that needs more than one reply to land a meet
ask. Her immediately pushing a relationship frame.

scoring under this goal: TODO — uses scoring overrides above until
field data accumulates.
