#!/usr/bin/env bash

set -euxo pipefail

uv generate-shell-completion zsh
uv sync --dev --all-extras
uv run pre-commit install --allow-missing-config

cat<<'A'>> ~/.zshrc
command -v deactivate &>/dev/null || . .venv/bin/activate
A

sed -i ~/.zshrc -e 's/^ZSH_THEME=.*/ZSH_THEME="refined"/'

[[ -d .venv ]] || uv venv
