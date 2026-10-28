#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$workspace_dir"

python3 -m pytest -q src/hospital_robot/test

echo
echo 'Validações estáticas concluídas.'
