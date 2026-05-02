#!/usr/bin/env bash
# dev.sh — one-shot quick start for local laptop development.
#
# What it does:
#   1. Creates a Python virtualenv in .venv (first run only)
#   2. Installs dependencies in editable mode
#   3. Creates .env from the example if it doesn't exist
#   4. Verifies your ANTHROPIC_API_KEY is set
#   5. Starts the web UI at http://127.0.0.1:7878 with auto-reload
#
# Usage:
#   ./dev.sh

set -euo pipefail

cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found. Install Python 3.12+." >&2
  exit 1
fi

# 1. venv
if [ ! -d .venv ]; then
  echo "==> creating .venv"
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

# 2. deps
if [ ! -f .venv/.deps_installed ] || [ pyproject.toml -nt .venv/.deps_installed ]; then
  echo "==> installing dependencies"
  pip install --quiet --upgrade pip
  pip install --quiet -e .
  touch .venv/.deps_installed
fi

# 3. .env
if [ ! -f .env ]; then
  echo "==> creating .env from .env.example"
  cp .env.example .env
  chmod 600 .env
  cat <<EOF

  Edit .env and paste your ANTHROPIC_API_KEY.
  Get one at https://console.anthropic.com/settings/keys

  Then re-run: ./dev.sh
EOF
  exit 0
fi

# 4. doctor
echo "==> dcp doctor"
dcp doctor || {
  echo
  echo "Fix the issues above (most likely: missing ANTHROPIC_API_KEY in .env), then re-run."
  exit 1
}

# 5. ui
echo
echo "==> starting web UI at http://127.0.0.1:7878"
echo "    open it in your browser; Ctrl-C to stop"
echo
exec dcp ui --reload
