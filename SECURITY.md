# Security notes

This is a personal tool that handles two kinds of sensitive data:

1. **Your Anthropic API key.** A leaked key lets a third party run charges
   against your account.
2. **The vault.** Real conversations, names, and personal context. Treat
   it like a private journal.

## API key handling

- The key is loaded from the `ANTHROPIC_API_KEY` environment variable.
  It is never read from a CLI flag, never logged, and never written to
  any file in this repo.
- For local development, put it in `.env` (gitignored). The CLI will
  load that file via `python-dotenv` if it exists.
- For Codespaces, set `ANTHROPIC_API_KEY` as a **Codespace secret** under
  the repository settings. The devcontainer declares it as a required
  secret and GitHub injects it as an env var.
- If `ANTHROPIC_API_KEY` is missing, the CLI exits with a clear error
  before any network call.
- The CLI sets `os.environ["ANTHROPIC_API_KEY"]` for the SDK and never
  passes the key as an argument to subprocesses.

## Repo hygiene

- `.gitignore` excludes `.env`, `.env.*` (except the example), and common
  secret-file patterns (`*.pem`, `*.key`, `*_secret*`, `*_credentials*`).
- Run `git status` before every commit. The agent's auto-commit only
  stages files inside `vault/`, so even if a stray `.env` ended up at
  repo root it would not be committed by the agent.
- Make the repo **private** on GitHub. The default for any new repo
  containing this should be private.

## If a key leaks

1. Rotate it immediately at https://console.anthropic.com/settings/keys
2. Update the Codespace secret and your local `.env`.
3. If it was committed: rotate first, then rewrite history with
   `git filter-repo` (or `git filter-branch`) and force-push. Rotation
   matters more than scrubbing history — assume any committed secret
   has been scraped.

## Vault privacy

- The repo should be **private**. There is no setting that protects you
  from an accidentally-public personal vault.
- If you sync via GitHub, your conversations are stored on GitHub's
  servers. That is the deployment trade-off documented in the design.
- If you want some vault content kept local-only, create
  `vault/private/` and uncomment the matching line in `.gitignore`.

## Threat model: what this does NOT defend against

- Anyone with read access to the repo (you, collaborators, GitHub
  staff under legal process). Use a private repo and don't add
  collaborators.
- Anyone with access to your machine or your Codespace.
- Prompt injection from pasted message content. The agent has file
  write access to the vault; a malicious paste could in theory direct
  it to rewrite files. Mitigation: review the diff before each commit
  (the auto-commit makes this trivially inspectable via `git log -p`).
