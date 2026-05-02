"""webui — lightweight FastAPI UI on top of the dcp agent runtime.

Runs locally (or in a Codespace with a forwarded port). Lets the user:
  - see all matches and their current phase
  - create a new match
  - paste her latest message and/or upload a screenshot
  - add per-turn context that gets injected into the orchestrator prompt
  - get suggestions, then mark which one was actually sent
  - label outcomes (replied warm / cold / no_reply / meet_set / dead)

The UI imports from `dcp` so the agent runtime, env handling, and
auto-commit all match the CLI exactly. There is no separate state.
"""

from __future__ import annotations

import asyncio
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from fastapi import FastAPI, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from markdown_it import MarkdownIt

import dcp

REPO_ROOT = Path(__file__).resolve().parent
TEMPLATES_DIR = REPO_ROOT / "templates"
STATIC_DIR = REPO_ROOT / "static"

app = FastAPI(title="dating-copilot")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

md_renderer = MarkdownIt("commonmark", {"html": False, "linkify": True, "breaks": True})
templates.env.filters["md"] = lambda text: md_renderer.render(text or "")


# ---------------------------------------------------------------------------
# Vault helpers — read-only parsing for display. Writes go through the agent.
# ---------------------------------------------------------------------------

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9\-]{0,80}$")


def _vault() -> Path:
    return dcp.vault_dir()


def _validate_slug(slug: str) -> None:
    """Refuse anything that could escape the matches/ directory."""
    if not SLUG_RE.match(slug):
        raise HTTPException(400, f"Invalid slug: {slug!r}")
    if slug.startswith("_") or slug == "screenshots":
        raise HTTPException(400, f"Reserved slug: {slug!r}")


def _match_path(slug: str) -> Path:
    _validate_slug(slug)
    p = (_vault() / "matches" / f"{slug}.md").resolve()
    # Guard against path traversal — must remain inside vault/matches.
    matches_dir = (_vault() / "matches").resolve()
    if matches_dir not in p.parents and p.parent != matches_dir:
        raise HTTPException(400, "Path traversal blocked")
    return p


def _parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    return meta, m.group(2)


def _list_matches() -> list[dict[str, Any]]:
    matches_dir = _vault() / "matches"
    if not matches_dir.exists():
        return []
    rows = []
    for f in sorted(matches_dir.glob("*.md")):
        if f.name.startswith("_"):
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except OSError:
            continue
        meta, _ = _parse_frontmatter(text)
        rows.append(
            {
                "slug": f.stem,
                "name": meta.get("name", f.stem),
                "city": meta.get("city", ""),
                "platform": meta.get("platform", ""),
                "phase": meta.get("phase", ""),
                "goal_type": meta.get("goal_type", ""),
                "days_remaining": meta.get("days_remaining", ""),
                "last_message_at": meta.get("last_message_at", ""),
            }
        )
    rows.sort(key=lambda r: str(r.get("last_message_at") or ""), reverse=True)
    return rows


def _read_match(slug: str) -> dict[str, Any]:
    path = _match_path(slug)
    if not path.exists():
        raise HTTPException(404, f"Match not found: {slug}")
    text = path.read_text(encoding="utf-8")
    meta, body = _parse_frontmatter(text)
    return {"slug": slug, "meta": meta, "body": body, "raw": text, "path": path}


def _save_screenshot(slug: str, upload: UploadFile) -> Path:
    """Persist an uploaded screenshot under vault/matches/screenshots/<slug>/."""
    if upload.content_type not in {"image/png", "image/jpeg", "image/webp", "image/gif"}:
        raise HTTPException(400, f"Unsupported screenshot type: {upload.content_type}")
    ext = {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "image/webp": ".webp",
        "image/gif": ".gif",
    }[upload.content_type]
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = _vault() / "matches" / "screenshots" / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{ts}{ext}"
    with out_path.open("wb") as f:
        # Cap at 8 MB. Mobile screenshots are < 1 MB; anything bigger is suspicious.
        max_bytes = 8 * 1024 * 1024
        written = 0
        while True:
            chunk = upload.file.read(64 * 1024)
            if not chunk:
                break
            written += len(chunk)
            if written > max_bytes:
                f.close()
                out_path.unlink(missing_ok=True)
                raise HTTPException(413, "Screenshot too large (max 8 MB)")
            f.write(chunk)
    return out_path


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "matches": _list_matches()},
    )


@app.post("/matches/new")
def create_match(
    slug: str = Form(...),
    name: str = Form(...),
    platform: str = Form(...),
    city: str = Form(...),
    days_remaining: str = Form(""),
    profile_notes: str = Form(""),
    context: str = Form(""),
):
    _validate_slug(slug)
    existing = _vault() / "matches" / f"{slug}.md"
    if existing.exists():
        raise HTTPException(409, f"Match already exists: {slug}")
    dcp.run_command(
        "new_match",
        {
            "MATCH": slug,
            "NAME": name,
            "PLATFORM": platform,
            "CITY": city,
            "DAYS_REMAINING": days_remaining or None,
            "PROFILE_NOTES": profile_notes or None,
        },
        context=context or None,
        commit_message=f"agent: new_match {slug}",
    )
    return RedirectResponse(f"/matches/{slug}", status_code=303)


@app.get("/matches/{slug}", response_class=HTMLResponse)
def match_detail(request: Request, slug: str, last_output: str = ""):
    match = _read_match(slug)
    return templates.TemplateResponse(
        "match.html",
        {
            "request": request,
            "match": match,
            "last_output": last_output,
            "modes": dcp.MODES,
        },
    )


@app.post("/matches/{slug}/suggest", response_class=HTMLResponse)
async def suggest(
    request: Request,
    slug: str,
    mode: str = Form("options"),
    her_message: str = Form(""),
    context: str = Form(""),
    screenshot: UploadFile | None = None,
):
    _validate_slug(slug)
    if mode not in dcp.MODES:
        raise HTTPException(400, f"Invalid mode: {mode}")

    screenshot_path: Path | None = None
    if screenshot is not None and screenshot.filename:
        screenshot_path = _save_screenshot(slug, screenshot)

    if not her_message and screenshot_path is None:
        raise HTTPException(400, "Provide a message, a screenshot, or both.")

    # Run the agent in a thread so we don't block the event loop.
    output = await asyncio.to_thread(
        dcp.run_command,
        "suggest",
        {
            "MATCH": slug,
            "MODE": mode,
            "HER_MESSAGE": her_message or None,
            "SCREENSHOT_PATH": str(screenshot_path) if screenshot_path else None,
        },
        context or None,
        f"agent: suggest for {slug}",
    )

    match = _read_match(slug)
    return templates.TemplateResponse(
        "match.html",
        {
            "request": request,
            "match": match,
            "last_output": output,
            "modes": dcp.MODES,
        },
    )


@app.post("/matches/{slug}/record-sent", response_class=HTMLResponse)
async def record_sent(
    request: Request,
    slug: str,
    chosen: str = Form(...),
    edited_text: str = Form(""),
    note: str = Form(""),
    context: str = Form(""),
):
    _validate_slug(slug)
    # If the user pasted edited text, that wins as the "chosen" value.
    chosen_value = edited_text.strip() if edited_text.strip() else chosen.strip()
    if not chosen_value:
        raise HTTPException(400, "Pick an option or paste the text you sent.")

    output = await asyncio.to_thread(
        dcp.run_command,
        "record_sent",
        {"MATCH": slug, "CHOSEN": chosen_value, "NOTE": note or None},
        context or None,
        f"agent: record_sent {slug}",
    )

    match = _read_match(slug)
    return templates.TemplateResponse(
        "match.html",
        {
            "request": request,
            "match": match,
            "last_output": output,
            "modes": dcp.MODES,
        },
    )


@app.post("/matches/{slug}/label", response_class=HTMLResponse)
async def label(
    request: Request,
    slug: str,
    outcome: str = Form(...),
    note: str = Form(""),
    context: str = Form(""),
):
    _validate_slug(slug)
    output = await asyncio.to_thread(
        dcp.run_command,
        "label",
        {"MATCH": slug, "OUTCOME": outcome, "NOTE": note or None},
        context or None,
        f"agent: label {slug} {outcome}",
    )
    match = _read_match(slug)
    return templates.TemplateResponse(
        "match.html",
        {
            "request": request,
            "match": match,
            "last_output": output,
            "modes": dcp.MODES,
        },
    )


@app.get("/matches/{slug}/screenshots/{name}")
def get_screenshot(slug: str, name: str):
    _validate_slug(slug)
    if not re.match(r"^[A-Za-z0-9._\-]{1,80}$", name):
        raise HTTPException(400, "Invalid screenshot name")
    path = (_vault() / "matches" / "screenshots" / slug / name).resolve()
    base = (_vault() / "matches" / "screenshots" / slug).resolve()
    if base not in path.parents:
        raise HTTPException(400, "Path traversal blocked")
    if not path.exists():
        raise HTTPException(404, "Not found")
    from fastapi.responses import FileResponse

    return FileResponse(path)
