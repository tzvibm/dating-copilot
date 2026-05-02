# Phase: escalation

Move from "we're chatting" to "we're meeting". Highest-stakes phase.
Mistiming kills it.

## You're in this phase when

- Rapport has produced at least one mutual question/answer pair where
  both sides volunteered something.
- She's responded within a reasonable window twice in a row.
- The conversation has a tone you'd be happy to continue in person.

## What works

- Anchoring to a time window, not a hard ask, when `days_remaining > 4`.
- Hard ask ("drinks Thursday at 8?") only when the rapport is loud
  and the window is short.
- Pairing the ask with one specific suggestion (place or activity).

## What doesn't

- Asking before mutual reciprocation.
- "We should grab a drink sometime" — sometime never happens.
- Stacking a long message + an ask. Make the ask its own line.

## Strategies in this phase

- `escalation-soft-time-anchor` — "I'm around Thursday-ish". Default
  when `days_remaining > 4` and she's not a planner type.
- `escalation-direct-ask` — "drinks Thursday at 8?". Use when window
  is short or she's a planner.
- `escalation-activity-anchor` — propose a specific activity she
  already mentioned wanting to do. Removes "what should we do"
  overhead.

## Goal-type interactions

- `quick-meet-window` — primary phase. Don't over-rapport.
- `flexible-short-window` — escalate only on her cue.
- `extended-window` — escalate when there's a reason (a specific
  upcoming thing), not arbitrarily.
- `decline-gracefully` — do not escalate; this phase is wrong for
  the goal.

## Phase exit

→ `logistics` — she said yes (explicit or near-explicit).
→ `recovery` — she went silent or cooled noticeably after the ask.
→ `dead` — explicit decline.
