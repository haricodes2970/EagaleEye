#!/usr/bin/env sh
# EagleEye installer — the npm -g equivalent for terminals without pipx.
set -eu

REPO="https://github.com/haricodes2970/EagaleEye.git"

if command -v pipx >/dev/null 2>&1; then
    pipx install "$REPO"
    echo "✓ installed — type: eye"
    exit 0
fi

echo "pipx not found → bootstrapping pipx into ~/.local"
python3 -m pip install --user pipx 2>/dev/null || python3 -m ensurepip --user || {
    echo "✗ need pip or pipx — install python3-pipx via your package manager"
    exit 1
}
python3 -m pipx ensurepath
python3 -m pipx install "$REPO"
echo "✓ installed — open a NEW terminal (or 'source ~/.bashrc') and type: eye"
