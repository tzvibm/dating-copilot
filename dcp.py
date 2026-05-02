"""dcp — Dating Copilot CLI.

Single-agent runtime over a markdown vault. The agent reads/writes vault
files via the Claude Agent SDK's built-in tools; this module is the glue
that loads config, configures the SDK, runs the loop, and commits the
resulting vault diff.

Security model: the Anthropic API key is read exclusively from the
ANTHROPIC_API_KEY environment variable (or a local .env file). It is
never logged, never accepted as a CLI flag, and never written to disk
by this module. See SECURITY.md.
"""

from __future__ import annotations

import asyncio
import os
import subprocess
import sys
from pathlib import Path

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_VAULT = REPO_ROOT / "vault"
ORCHESTRATOR_PROMPT = REPO_ROOT / "prompts" / "orchestrator.md"

app = typer.Typer(
    add_completion=False,
    help="Dating Copilot — agent-driven suggestions over a markdown vault.",
    no_args_is_help=True,
)
console = Console(stderr=False)
err = Console(stderr=True)


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


def load_env() -> None:
    """Load .env if present. Codespaces injects secrets directly so the
    file is optional. Never overrides values already in the environment.
    """
    env_path = REPO_ROOT / ".env"
    if env_path.exists():
        if os.name == "posix":
            mode = env_path.stat().st_mode & 0o777
            if mode & 0o077:
                err.print(
                    f"[red]Refusing to load {env_path}: file mode is "
                    f"{oct(mode)}. Run `chmod 600 .env` and retry.[/red]"
                )
                raise typer.Exit(code=2)
        load_dotenv(env_path, override=False)


def require_api_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        err.print(
            "[red]ANTHROPIC_API_KEY is not set.[/red]\n"
            "  - Local: copy .env.example to .env and paste your key, "
            "then `chmod 600 .env`.\n"
            "  - Codespaces: add ANTHROPIC_API_KEY as a Codespace secret "
            "in the repo settings.\n"
            "  Get a key at https://console.anthropic.com/settings/keys"
        )
        raise typer.Exit(code=2)
    if not key.startswith("sk-"):
        err.print(
            "[yellow]Warning: ANTHROPIC_API_KEY does not look like an "
            "Anthropic key (expected prefix 'sk-'). Continuing anyway.[/yellow]"
        )
    return key


def vault_dir() -> Path:
    override = os.environ.get("DCP_VAULT_DIR", "").strip()
    path = Path(override).expanduser().resolve() if override else DEFAULT_VAULT
    if not path.exists():
        err.print(f"[red]Vault directory not found: {path}[/red]")
        raise typer.Exit(code=2)
    return path


def model_id() -> str:
    return os.environ.get("DCP_MODEL", "claude-opus-4-7").strip()


def autocommit_enabled() -> bool:
    return os.environ.get("DCP_AUTOCOMMIT", "1") not in ("0", "false", "False", "")


def autopush_enabled() -> bool:
    return os.environ.get("DCP_AUTOPUSH", "1") not in ("0", "false", "False", "")


# ---------------------------------------------------------------------------
# Git
# ---------------------------------------------------------------------------


def _git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def _has_vault_changes(vault: Path) -> bool:
    res = _git(["status", "--porcelain", "--", str(vault)])
    return bool(res.stdout.strip())


def autocommit(vault: Path, message: str) -> None:
    if not autocommit_enabled():
        return
    if not _has_vault_changes(vault):
        return
    # Only stage paths inside the vault. Never `git add -A`: that would
    # risk staging a stray .env at repo root.
    _git(["add", "--", str(vault)])
    commit = _git(["commit", "-m", message])
    if commit.returncode != 0:
        err.print(f"[yellow]auto-commit skipped: {commit.stderr.strip()}[/yellow]")
        return
    console.print(f"[dim]committed: {message}[/dim]")
    if autopush_enabled():
        push = _git(["push"])
        if push.returncode != 0:
            err.print(
                f"[yellow]auto-push failed (changes are committed locally): "
                f"{push.stderr.strip()}[/yellow]"
            )


# ---------------------------------------------------------------------------
# Agent runtime (importable by the web UI)
# ---------------------------------------------------------------------------


def orchestrator_prompt() -> str:
    if not ORCHESTRATOR_PROMPT.exists():
        raise FileNotFoundError(f"Missing system prompt: {ORCHESTRATOR_PROMPT}")
    return ORCHESTRATOR_PROMPT.read_text(encoding="utf-8")


def _extract_text(message: object) -> str:
    """Pull plain text out of an SDK message in a shape-tolerant way."""
    content = getattr(message, "content", None)
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            text = getattr(block, "text", None)
            if isinstance(text, str):
                parts.append(text)
            elif isinstance(block, dict) and isinstance(block.get("text"), str):
                parts.append(block["text"])
        return "".join(parts)
    return ""


async def run_agent(user_message: str, vault: Path) -> str:
    """Run a single agent turn. Returns the assistant's final text."""
    # Deferred import so --help and config errors don't require the SDK.
    from claude_agent_sdk import ClaudeAgentOptions, query

    options = ClaudeAgentOptions(
        system_prompt=orchestrator_prompt(),
        cwd=str(vault),
        model=model_id(),
        allowed_tools=["Read", "Write", "Edit", "Glob", "Grep", "Bash"],
        permission_mode="acceptEdits",
    )

    chunks: list[str] = []
    async for message in query(prompt=user_message, options=options):
        text = _extract_text(message)
        if text:
            chunks.append(text)
    return "".join(chunks).strip()


def build_user_message(
    command: str,
    fields: dict[str, str | None],
    context: str | None = None,
) -> str:
    """Assemble the structured user message the orchestrator parses.

    `command` is one of: suggest, label, review, record_sent, new_match.
    `fields` is an ordered map of UPPER_CASE_KEY -> value; None values
    are skipped. `context` is the optional per-turn user context block.
    """
    parts = [f"COMMAND: {command}"]
    for key, value in fields.items():
        if value is None or value == "":
            continue
        if "\n" in value:
            parts.append(f"{key}:\n{value}")
        else:
            parts.append(f"{key}: {value}")
    if context:
        parts.append(f"USER_CONTEXT:\n{context.strip()}")
    return "\n\n".join(parts)


def run_command(
    command: str,
    fields: dict[str, str | None],
    context: str | None = None,
    commit_message: str | None = None,
) -> str:
    """High-level entry point used by both the CLI and the UI."""
    load_env()
    require_api_key()
    vault = vault_dir()
    user_message = build_user_message(command, fields, context)
    output = asyncio.run(run_agent(user_message, vault))
    if commit_message:
        autocommit(vault, commit_message)
    return output


# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------


MODES = ("draft", "options", "coach")


def _read_stdin_if_tty(prompt: str) -> str:
    console.print(f"[dim]{prompt}[/dim]")
    return sys.stdin.read().strip()


@app.command()
def suggest(
    match: str = typer.Argument(..., help="Match slug, e.g. 2026-04-sofia-cr"),
    mode: str = typer.Option("options", "--mode", "-m", help=f"One of: {', '.join(MODES)}"),
    message: str = typer.Option(
        "",
        "--message",
        "-M",
        help="Her latest message. If omitted and no screenshot, prompted from stdin.",
    ),
    screenshot: Path | None = typer.Option(
        None,
        "--screenshot",
        "-s",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Path to a screenshot of the latest message(s).",
    ),
    context: str = typer.Option(
        "",
        "--context",
        "-c",
        help="Free-form per-turn context to inject into the orchestrator prompt.",
    ),
) -> None:
    """Generate suggestions for the next message to a match."""
    if mode not in MODES:
        err.print(f"[red]--mode must be one of: {', '.join(MODES)}[/red]")
        raise typer.Exit(code=2)

    if not message and screenshot is None:
        message = _read_stdin_if_tty(
            "Paste her message. End with a blank line + Ctrl-D (Unix) or Ctrl-Z+Enter (Windows)."
        )

    output = run_command(
        "suggest",
        {
            "MATCH": match,
            "MODE": mode,
            "HER_MESSAGE": message or None,
            "SCREENSHOT_PATH": str(screenshot.resolve()) if screenshot else None,
        },
        context=context or None,
        commit_message=f"agent: suggest for {match}",
    )
    if output:
        console.print(Markdown(output))


@app.command(name="record-sent")
def record_sent(
    match: str = typer.Argument(..., help="Match slug."),
    chosen: str = typer.Argument(
        ...,
        help="Chosen suggestion id (1, 2, 3) OR verbatim text actually sent.",
    ),
    note: str = typer.Option("", "--note", "-n", help="Optional note."),
    context: str = typer.Option("", "--context", "-c", help="Per-turn context."),
) -> None:
    """Record that a suggested message (or an edited version) was sent."""
    output = run_command(
        "record_sent",
        {"MATCH": match, "CHOSEN": chosen, "NOTE": note or None},
        context=context or None,
        commit_message=f"agent: record_sent {match}",
    )
    if output:
        console.print(Markdown(output))


@app.command()
def label(
    match: str = typer.Argument(..., help="Match slug."),
    outcome: str = typer.Argument(
        ...,
        help="replied_warm | replied_cold | no_reply | meet_set | meet_happened | dead",
    ),
    note: str = typer.Option("", "--note", "-n", help="Optional note."),
    context: str = typer.Option("", "--context", "-c", help="Per-turn context."),
) -> None:
    """Label the outcome of the previous turn."""
    output = run_command(
        "label",
        {"MATCH": match, "OUTCOME": outcome, "NOTE": note or None},
        context=context or None,
        commit_message=f"agent: label {match} {outcome}",
    )
    if output:
        console.print(Markdown(output))


@app.command()
def review(
    match: str = typer.Argument(..., help="Match slug."),
    context: str = typer.Option("", "--context", "-c", help="Per-turn context."),
) -> None:
    """Read state, summarise, recommend a next move (no draft)."""
    output = run_command(
        "review",
        {"MATCH": match},
        context=context or None,
        commit_message=f"agent: review {match}",
    )
    if output:
        console.print(Markdown(output))


@app.command(name="new-match")
def new_match(
    slug: str = typer.Argument(..., help="Match slug, e.g. 2026-05-sofia-cr"),
    name: str = typer.Option(..., "--name", help="Her first name."),
    platform: str = typer.Option(..., "--platform", help="tinder | hinge | bumble | feeld | other"),
    city: str = typer.Option(..., "--city", help="Human-readable city."),
    days_remaining: int | None = typer.Option(
        None,
        "--days-remaining",
        help="Days left in the current overlap window.",
    ),
    profile_notes: str = typer.Option("", "--profile-notes", help="What you noticed in her profile."),
    context: str = typer.Option("", "--context", "-c", help="Per-turn context."),
) -> None:
    """Bootstrap a match file from minimal info."""
    output = run_command(
        "new_match",
        {
            "MATCH": slug,
            "NAME": name,
            "PLATFORM": platform,
            "CITY": city,
            "DAYS_REMAINING": str(days_remaining) if days_remaining is not None else None,
            "PROFILE_NOTES": profile_notes or None,
        },
        context=context or None,
        commit_message=f"agent: new_match {slug}",
    )
    if output:
        console.print(Markdown(output))


@app.command()
def ui(
    host: str = typer.Option("127.0.0.1", "--host", help="Bind host. Use 0.0.0.0 in Codespaces."),
    port: int = typer.Option(7878, "--port", help="Port."),
) -> None:
    """Launch the lightweight web UI."""
    load_env()
    require_api_key()  # fail fast before starting uvicorn

    try:
        import uvicorn  # noqa: F401
    except ImportError:
        err.print(
            "[red]uvicorn is not installed.[/red] Install UI deps: "
            "`pip install -e '.[ui]'`"
        )
        raise typer.Exit(code=2) from None

    # In Codespaces, default to all-interfaces so the port-forwarding works.
    if os.environ.get("CODESPACES") == "true" and host == "127.0.0.1":
        host = "0.0.0.0"

    console.print(
        f"[green]dcp ui[/green] starting at http://{host}:{port} "
        f"(vault: {vault_dir()})"
    )
    import uvicorn

    uvicorn.run("webui:app", host=host, port=port, log_level="info", reload=False)


@app.command()
def doctor() -> None:
    """Report on environment and config without making any API calls."""
    load_env()
    issues = 0

    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        err.print("[red]x ANTHROPIC_API_KEY not set[/red]")
        issues += 1
    else:
        masked = f"{key[:5]}...{key[-4:]}" if len(key) > 12 else "set"
        console.print(f"[green]✓[/green] ANTHROPIC_API_KEY {masked}")

    vault = REPO_ROOT / "vault"
    override = os.environ.get("DCP_VAULT_DIR", "").strip()
    if override:
        vault = Path(override).expanduser().resolve()
    if vault.exists():
        console.print(f"[green]✓[/green] vault: {vault}")
    else:
        err.print(f"[red]x vault not found: {vault}[/red]")
        issues += 1

    if ORCHESTRATOR_PROMPT.exists():
        console.print(f"[green]✓[/green] orchestrator prompt: {ORCHESTRATOR_PROMPT}")
    else:
        err.print(f"[red]x orchestrator prompt missing: {ORCHESTRATOR_PROMPT}[/red]")
        issues += 1

    env_path = REPO_ROOT / ".env"
    if env_path.exists() and os.name == "posix":
        mode = env_path.stat().st_mode & 0o777
        if mode & 0o077:
            err.print(
                f"[red]x .env has loose permissions ({oct(mode)}); "
                f"run `chmod 600 .env`[/red]"
            )
            issues += 1
        else:
            console.print(f"[green]✓[/green] .env permissions {oct(mode)}")

    console.print(f"[dim]model: {model_id()}[/dim]")
    console.print(
        f"[dim]autocommit: {autocommit_enabled()}  autopush: {autopush_enabled()}[/dim]"
    )

    if issues:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
