#!/bin/bash
# Porțile unei teme: citate verbatim (build), audit determinist, poarta semantică, banda de triaj ≥ 0,50.
# Utilizare: bash poarta_tema.sh 07
cd "$(dirname "$0")" || exit 1
set -o pipefail
N=$(printf "%02d" "$((10#$1))")
python3 tematica_build.py | grep -E "^tema $((10#$1)):|EROARE|ATENȚIE|nimic scris" || exit 1
python3 audit_tematica.py "$N" || exit 1
./.venv-ts/bin/python check_tematica.py "$N" | tail -12 || exit 1
python3 triaj_tema.py "$N"
