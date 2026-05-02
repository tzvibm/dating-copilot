# dating-copilot

Personal copilot for moving dating-app conversations from first message
to an in-person meet. Single-agent system with a markdown vault for state,
git for history, optional web UI for phone use.

> Personal tool. Single user. Make the repo private.

## What's here

```
dcp.py                # CLI (suggest, record-sent, label, review, new-match, ui, doctor)
webui.py              # FastAPI app behind `dcp ui`
prompts/
  orchestrator.md     # the system prompt that drives the agent
templates/, static/   # the web UI
vault/                # the agent's memory: markdown + frontmatter
.devcontainer/        # Codespaces setup with required secret declared
.env.example          # template; copy to .env locally
SECURITY.md           # threat model + key handling
```

## Setup

### Local

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
cp .env.example .env
chmod 600 .env                    # required; the CLI refuses loose perms
$EDITOR .env                      # paste your ANTHROPIC_API_KEY
dcp doctor                        # verify config
```

Get an Anthropic key at https://console.anthropic.com/settings/keys.

### GitHub Codespaces

1. Push this repo to GitHub. **Make it private.**
2. Repo → Settings → Secrets and variables → Codespaces → New repository
   secret. Name: `ANTHROPIC_API_KEY`. Paste the key.
3. Open the repo in a Codespace. The devcontainer declares the secret
   as required, so GitHub injects it as an env var. No `.env` file
   needed; do not create one in the Codespace.
4. In the Codespace terminal: `dcp doctor`.

## Usage

### CLI

```bash
# bootstrap a match
dcp new-match 2026-05-sofia-cr --name Sofia --platform tinder \
  --city "San José, CR" --days-remaining 9 \
  --profile-notes "bookstore pic, mentions she's here 6 weeks"

# get suggestions for the next message (paste her message at the prompt,
# Ctrl-D when done)
dcp suggest 2026-05-sofia-cr --mode options

# pass per-turn context to the agent
dcp suggest 2026-05-sofia-cr -c "I'm flying out Saturday so timing is tight"

# screenshot instead of pasted text
dcp suggest 2026-05-sofia-cr -s ~/Downloads/screen.png

# record what you actually sent (1, 2, or 3 from the suggestions, or
# the verbatim text if you edited)
dcp record-sent 2026-05-sofia-cr 2

# label the outcome after she replies (or doesn't)
dcp label 2026-05-sofia-cr replied_warm

# read the state and recommend a next move (no draft)
dcp review 2026-05-sofia-cr
```

Every command auto-commits the vault diff to git and pushes (assuming
the branch tracks an upstream). Disable with `DCP_AUTOCOMMIT=0` /
`DCP_AUTOPUSH=0`.

### Web UI

```bash
dcp ui                # http://127.0.0.1:7878
```

In a Codespace, `dcp ui` binds to `0.0.0.0` automatically and the port
is forwarded; open the forwarded URL from your phone. The UI lets you:

- create matches with a small form
- paste messages or upload screenshots
- add per-turn context that gets injected into the agent prompt
- pick a suggestion (1/2/3) or paste an edited version, mark it sent
- record outcome labels

The UI calls the same agent runtime as the CLI, so commits and history
stay consistent.

## How the agent works

- **One agent, one system prompt, one loop.** `prompts/orchestrator.md`
  is the entire program logic.
- **The vault is the state.** Markdown with YAML frontmatter. Read with
  your eyes in any markdown viewer.
- **Tools the agent has:** Read, Write, Edit, Glob, Grep, Bash. No MCP
  servers, no databases.
- **Git is the audit trail.** Every command auto-commits. Use `git log`
  / `git diff` / `git revert` like normal.
- **Hard rules:** the agent never edits `vault/identity.md`, never
  sends messages, never runs git commands, and never touches files
  outside the vault.

See [the design doc](./docs/) (or the conversation that produced this
repo) for the full rationale.

## Security

- API key is loaded only from `ANTHROPIC_API_KEY`. Never logged. Never
  written to disk by this code. Never accepted as a CLI flag.
- The CLI refuses to read a `.env` with loose permissions on POSIX.
- Auto-commit only stages files inside `vault/` — a stray secret at
  repo root is not picked up.
- Make the repo **private**. The vault contains real names and
  conversations.
- See [SECURITY.md](./SECURITY.md) for the full threat model.

## Customising

- **Voice.** Replace the placeholders in `vault/self/voice.md` with
  ~10 real messages you've sent. The agent calibrates from these.
- **Identity.** Fill in `vault/identity.md` by hand. Set the default
  match goal at the bottom. The agent reads this every turn but never
  writes to it.
- **Goals.** `vault/goals/_archetypes.md` is a small fixed list. Edit
  it — but sparingly. Strategy cards reference these ids.
- **Strategies.** `vault/strategies/` contains opener and escalation
  examples. Copy and edit. `compatible_goals` / `incompatible_goals`
  determine which strategies are filtered out for a given match.
- **City files.** `vault/cities/_template.md` is the schema. Drop new
  ones in for each city you spend time in.

## Troubleshooting

- `dcp doctor` reports config without making API calls.
- If auto-push fails, the commit is still local; push by hand.
- If the agent says a match file is missing, run `dcp new-match` first.
- If suggestions feel generic, your `voice.md` is empty or thin —
  paste real messages.

## License

Personal tool. Don't redistribute.
