#!/usr/bin/env bash
# dev.sh — one-shot quick start for local laptop development.
#
# What it does:
#   1. Verifies you have Python 3.12+
#   2. Creates a Python virtualenv in .venv (first run only)
#   3. Installs dependencies in editable mode (re-runs if pyproject.toml
#      changed)
#   4. Creates .env from the example if it doesn't exist, prompts you
#      to paste your key, then exits
#   5. On re-run with key set: runs `dcp doctor`, then starts the web
#      UI at http://127.0.0.1:7878 with auto-reload
#
# Usage:
#   ./dev.sh

set -euo pipefail

cd "$(dirname "$0")"

# ---------------------------------------------------------------------------
# 0. Python version check
# ---------------------------------------------------------------------------

if ! command -v python3 >/dev/null 2>&1; then
  cat >&2 <<EOF
ERROR: python3 not found.

  macOS:    brew install python@3.12
  Ubuntu:   sudo apt install python3.12 python3.12-venv
  Other:    https://www.python.org/downloads/
EOF
  exit 1
fi

PY_OK=$(python3 -c 'import sys; print(1 if sys.version_info >= (3, 12) else 0)')
PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")')
if [ "$PY_OK" != "1" ]; then
  cat >&2 <<EOF
ERROR: Python 3.12+ required (found $PY_VER).

  macOS:    brew install python@3.12
            (then close + reopen the terminal so PATH refreshes)
  Ubuntu:   sudo apt install python3.12 python3.12-venv
EOF
  exit 1
fi

# ---------------------------------------------------------------------------
# 1. venv
# ---------------------------------------------------------------------------

if [ ! -d .venv ]; then
  echo "==> creating .venv (Python $PY_VER)"
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

# ---------------------------------------------------------------------------
# 2. deps (re-install if pyproject.toml changed)
# ---------------------------------------------------------------------------

if [ ! -f .venv/.deps_installed ] || [ pyproject.toml -nt .venv/.deps_installed ]; then
  echo "==> installing dependencies"
  pip install --quiet --upgrade pip
  pip install --quiet -e .
  touch .venv/.deps_installed
fi

# ---------------------------------------------------------------------------
# 3. .env
# ---------------------------------------------------------------------------

if [ ! -f .env ]; then
  echo "==> creating .env from .env.example"
  cp .env.example .env
  chmod 600 .env
  cat <<EOF

  Almost done. Edit .env and paste your ANTHROPIC_API_KEY:

    \$EDITOR .env
    # or: nano .env, code .env, vim .env, etc.

  Get a key at https://console.anthropic.com/settings/keys

  Then re-run:

    ./dev.sh

EOF
  exit 0
fi

# ---------------------------------------------------------------------------
# 4. config check
# ---------------------------------------------------------------------------

echo "==> dcp doctor"
dcp doctor || {
  cat >&2 <<EOF

Fix the issues above (most likely: missing ANTHROPIC_API_KEY in .env),
then re-run ./dev.sh
EOF
  exit 1
}

# ---------------------------------------------------------------------------
# 5. ui
# ---------------------------------------------------------------------------

cat <<EOF

==> starting web UI at http://127.0.0.1:7878
    open it in your browser, then tap "run setup" to do the
    onboarding interview. Ctrl-C here to stop.

EOF
exec dcp ui --reload
