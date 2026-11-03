#!/usr/bin/env sh
# EagleEye auto-installer — always latest from main.
# Run once to install; run again to upgrade to the newest commit.
set -eu

REPO="https://github.com/haricodes2970/EagaleEye.git"

if ! command -v pipx >/dev/null 2>&1; then
    echo "[eagaleeye] pipx missing → bootstrapping"
    python3 -m pip install --user pipx 2>/dev/null || python3 -m ensurepip --user || {
        echo "✗ install python3-pipx then re-run"; exit 1
    }
    python3 -m pipx ensurepath
fi

echo "[eagaleeye] refreshing to latest ($REPO)"
pipx uninstall -y eagaleeye >/dev/null 2>&1 || true
pipx install "$REPO"

echo "✓ done — open a NEW terminal (or 'source ~/.bashrc') and type:  eye"
