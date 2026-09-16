#!/usr/bin/env bash
set -euo pipefail
case "${1:-}" in
  build|install|test|bench)
    printf '%s\n' 'TODO: NPU workflow is not connected.' >&2
    printf '%s\n' 'Read docs/ENVIRONMENT.md; record device/CANN/sample versions, then implement this entry point.' >&2
    exit 2
    ;;
  *) printf '%s\n' 'Usage: bash scripts/npu.sh {build|install|test|bench}' >&2; exit 2 ;;
esac
