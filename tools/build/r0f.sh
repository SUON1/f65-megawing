#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
exec python3 "$root/tools/diagnostics/r0f_build.py" "${1:-}"
