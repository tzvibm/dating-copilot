# dating-copilot

Personal copilot for moving dating-app conversations from first message
to an in-person meet. FastAPI web UI on top of a single-agent runtime
over a markdown vault. Git is the audit trail.

> Personal tool. Single user. Make the repo private.

## Quick start (laptop)

You'll need Python 3.12+ and an Anthropic API key.

```bash
git clone <your-fork-url> dating-copilot
cd dating-copilot
./dev.sh
```

`dev.sh` creates a virtualenv, installs deps, drops a `.env` from the
template, then prints what to do next. Edit `.env`, paste your key
from https://console.anthropic.com/settings/keys, re-run `./dev.sh`,
and the web UI opens at **http://127.0.0.1:7878**.

First time using it: tap the orange **run setup** banner. The agent
interviews you for ~5 minutes and writes your `identity.md`,
`self/voice.md`, and `self/preferences.md`.

### Manual setup (if you want to do it without the script)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
cp .env.example .env
chmod 600 .env                       # required; CLI refuses loose perms
$EDITOR .env                         # paste ANTHROPIC_API_KEY=sk-...
dcp doctor                           # confirms the key is loaded
dcp setup                            # interview to fill identity/voice/prefs
dcp ui                               # http://127.0.0.1:7878
```

## What's here

```
dcp.py                # CLI: setup, suggest, record-sent, label, review,
                      #      new-match, ui, doctor
webui.py              # FastAPI app behind `dcp ui`
prompts/
  orchestrator.md     # system prompt for normal turns
  setup.md            # system prompt for the onboarding interview
templates/, static/   # the web UI
vault/                # the agent's memory: markdown + frontmatter
.env.example          # template; copy to .env and edit
SECURITY.md           # threat model + key handling
.devcontainer/        # Codespaces config (optional, for later mobile use)
```

## Usage

### Web UI (the main path)

```bash
dcp ui                # http://127.0.0.1:7878
dcp ui --reload       # auto-restart on code changes (dev)
```

The UI lets you:

- **Setup**: interview-driven onboarding (writes identity/voice/preferences).
- **Matches**: list, create, click into a match.
- **Suggest**: paste her message or upload a screenshot, optionally
  add per-turn context (e.g. "I'm flying out Saturday"), pick a mode
  (draft / options / coach), get suggestions.
- **Record sent**: tap the option you actually sent (1, 2, 3) or paste
  the verbatim text if you edited it. The agent records it.
- **Label outcome**: replied warm / cold / no_reply / meet_set / etc.
  Updates strategy stats.

Every action auto-commits the vault diff to git.

### CLI

Useful when you'd rather stay in the terminal:

```bash
# bootstrap a match
dcp new-match 2026-05-sofia-cr --name Sofia --platform tinder \
  --city "San José, CR" --days-remaining 9 \
  --profile-notes "bookstore pic, mentions she's here 6 weeks"

# get suggestions
dcp suggest 2026-05-sofia-cr --mode options
dcp suggest 2026-05-sofia-cr -c "she just said her trip got extended"
dcp suggest 2026-05-sofia-cr -s ~/Downloads/screen.png

# record what you sent (1, 2, or 3 from the suggestions)
dcp record-sent 2026-05-sofia-cr 2

# label outcome
dcp label 2026-05-sofia-cr replied_warm

# state-of-the-conversation summary, no draft
dcp review 2026-05-sofia-cr
```

`dcp doctor` reports config without making API calls.

## How the agent works

- **One agent, one system prompt, one loop.** `prompts/orchestrator.md`
  is the entire program logic for normal turns; `prompts/setup.md` is
  used only for the onboarding interview.
- **The vault is the state.** Markdown with YAML frontmatter. Read
  with your eyes in any markdown viewer.
- **Tools the agent has:** Read, Write, Edit, Glob, Grep, Bash. No
  MCP servers, no databases.
- **Git is the audit trail.** Every command auto-commits. Use
  `git log` / `git diff` / `git revert` like normal.
- **Hard rules:** the agent never edits `vault/identity.md` outside
  setup, never sends messages, never runs git, and never touches
  files outside the vault.

## Security

- API key is loaded only from `ANTHROPIC_API_KEY` (env or `.env`).
  Never logged. Never written to disk by this code. Never accepted
  as a CLI flag.
- The CLI refuses to read a `.env` with loose permissions on POSIX.
- Auto-commit only stages files inside `vault/` — a stray secret at
  repo root won't be picked up.
- The web UI binds to `127.0.0.1` by default — local-only. Don't
  change that unless you know why.
- Make the repo **private** before pushing. The vault contains real
  names and conversations.
- See [SECURITY.md](./SECURITY.md) for the full threat model.

## Customising

- **Voice / identity / preferences.** Use the `/setup` page (or
  `dcp setup`). Hand-editing those three files works too, but the
  interview is the intended path.
- **Goals.** `vault/goals/_archetypes.md` is a small fixed list. Edit
  it sparingly. Strategy cards reference these ids.
- **Strategies.** `vault/strategies/` contains opener and escalation
  examples. Copy and edit. `compatible_goals` /
  `incompatible_goals` filter which strategies the agent considers
  for a given match.
- **City files.** `vault/cities/_template.md` is the schema. Drop
  one in for each city you spend real time in.

## Deploying later

Today this runs on your laptop only. Options for later:

- **Mobile from anywhere via GitHub Codespaces.** A `.devcontainer/`
  is included. Push the repo (private), set `ANTHROPIC_API_KEY` as a
  Codespace secret, open in Codespaces from your phone browser, run
  `dcp ui --host 0.0.0.0`. Cold-start adds ~30s.
- **Tiny VPS / Render / Fly / Railway.** It's just a FastAPI app
  with a writable filesystem. The vault would need to live on a
  persistent volume, and you'd want to put the UI behind auth (it
  has none right now — fine for localhost, NOT for the internet).

Don't expose this to the public internet without adding auth.

## Troubleshooting

- `dcp doctor` reports config without making API calls.
- "ANTHROPIC_API_KEY not set" → check `.env` exists and has the key.
- Auto-push failure → the commit is still local; push by hand.
- "match file not found" → run `dcp new-match` first.
- Suggestions feel generic → your `voice.md` is empty or thin. Run
  `dcp setup` again and paste real messages.

## License

Personal tool. Don't redistribute.
