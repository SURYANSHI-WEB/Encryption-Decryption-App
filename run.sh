#!/usr/bin/env bash
# Lightweight entrypoint for quick demos.
# Tries to activate a local virtualenv if present, then runs examples.

set -e

if [ -f "venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  source "venv/bin/activate"
fi

python -m src.cli examples

# Exit codes: 0 success, non-zero if CLI fails.


