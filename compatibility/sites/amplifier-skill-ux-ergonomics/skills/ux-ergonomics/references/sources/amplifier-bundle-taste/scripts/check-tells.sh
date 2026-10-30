#!/usr/bin/env bash
#
# check-tells.sh — Greps source files for banned design patterns from this bundle's
# AI-tells list. Pure bash, no Python deps. Exit 1 if Critical violations found.
#
# Usage:
#   ./scripts/check-tells.sh [path]      # defaults to ./src
#   ./scripts/check-tells.sh --severity=critical|warning|all
#
# Used by: GitHub Actions workflow + manual audits. Complements the
# `taste:design-critic` agent (which does the same audit at the model level
# with richer reasoning).

set -euo pipefail

TARGET="${1:-src}"
SEVERITY="${SEVERITY:-critical}"

if [[ "${1:-}" == --severity=* ]]; then
  SEVERITY="${1#--severity=}"
  TARGET="${2:-src}"
fi

if [[ ! -d "$TARGET" ]]; then
  echo "error: target path '$TARGET' does not exist" >&2
  exit 2
fi

# File extensions to scan
EXTS=("tsx" "jsx" "vue" "svelte" "css" "scss" "html")

# Build the find command for relevant files
FIND_ARGS=()
for ext in "${EXTS[@]}"; do
  FIND_ARGS+=(-name "*.${ext}" -o)
done
unset 'FIND_ARGS[-1]'   # drop trailing -o

# Banned patterns — Critical severity (correctness or LLM-default tells)
declare -a CRITICAL_PATTERNS=(
  'font-family.*Inter[^-]'                 # Inter as body/UI default (brutalist Black is exception — manual check)
  '#000000\b'                              # pure black banned (use #0a0a0a etc)
  '\bh-screen\b'                           # iOS Safari viewport bug
  "window\\.addEventListener\\(['\"]scroll" # use IntersectionObserver
  'from-purple-[0-9].*to-(blue|indigo)'    # AI gradient (purple→blue)
  'from-blue-[0-9].*to-purple'             # AI gradient (blue→purple)
  '//\s*\.\.\.\s*$'                        # // ... placeholder
  '//\s*rest of'                           # // rest of code
  '#\s*TODO:?\s+implement'                 # placeholder TODO in committed code
)

# Banned patterns — Warning severity
declare -a WARNING_PATTERNS=(
  'rounded-full.*card|card.*rounded-full' # rounded-full on large containers (minimalist ban)
  'z-50\b'                                # z-index spam
  'Acme|Nexus|John Doe|Jane Doe'          # placeholder names
)

violations=0
critical_violations=0

scan_pattern() {
  local pattern="$1"
  local label="$2"
  while IFS= read -r match; do
    [[ -z "$match" ]] && continue
    echo "  [${label}] ${match}"
    violations=$((violations + 1))
    [[ "$label" == "CRITICAL" ]] && critical_violations=$((critical_violations + 1))
  done < <(find "$TARGET" \( "${FIND_ARGS[@]}" \) -type f -print0 2>/dev/null \
    | xargs -0 grep -nE "$pattern" 2>/dev/null || true)
}

echo "=== check-tells.sh — scanning '$TARGET' (severity: $SEVERITY) ==="
echo

if [[ "$SEVERITY" == "critical" || "$SEVERITY" == "all" ]]; then
  echo "--- Critical patterns ---"
  for p in "${CRITICAL_PATTERNS[@]}"; do
    scan_pattern "$p" "CRITICAL"
  done
fi

if [[ "$SEVERITY" == "warning" || "$SEVERITY" == "all" ]]; then
  echo
  echo "--- Warning patterns ---"
  for p in "${WARNING_PATTERNS[@]}"; do
    scan_pattern "$p" "WARNING"
  done
fi

echo
echo "=== Summary ==="
echo "Total violations: $violations (Critical: $critical_violations)"
echo
echo "For richer audits with archetype awareness, use the design-critic agent:"
echo "  amplifier --bundle taste task taste:design-critic 'audit ${TARGET}'"
echo

# Exit non-zero if Critical violations and severity covers Critical
if [[ "$critical_violations" -gt 0 && ( "$SEVERITY" == "critical" || "$SEVERITY" == "all" ) ]]; then
  exit 1
fi
exit 0
