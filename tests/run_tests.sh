#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
export PYTHONDONTWRITEBYTECODE=1
category="${1:-all}"
case "$category" in
    all) [[ $# -eq 0 ]] || shift; exec python -m pytest "$@" ;;
    unit|integration) shift; exec python -m pytest -m "$category" "$@" ;;
    *) exec python -m pytest "$@" ;;
esac
