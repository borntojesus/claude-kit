#!/usr/bin/env bash
# Fetch a brand/company logo, preferring SVG, falling back to PNG.
# Usage: fetch-logo.sh <slug> [domain] [outdir]
#   slug   : filename + simple-icons slug attempt (e.g. "sanity", "openzeppelin")
#   domain : canonical domain for clearbit/favicon (e.g. "openzeppelin.com")
#   outdir : where to save (default ./logos/co)
#
# Tries: simple-icons (SVG, monochrome/tint-ready) -> clearbit (PNG) -> favicon (PNG).
# Wikimedia / Brandfetch / press-kit hits: resolve the URL by hand and curl -L it.
# ALWAYS validate the result (this script does a basic sanity check and prints it).
set -euo pipefail

slug="${1:?usage: fetch-logo.sh <slug> [domain] [outdir]}"
domain="${2:-}"
outdir="${3:-./logos/co}"
mkdir -p "$outdir"

ua="Mozilla/5.0 (logo-finder)"
ok() { printf '✓ %s\n' "$1"; }
no() { printf '· %s\n' "$1"; }

is_svg()  { head -c 256 "$1" 2>/dev/null | grep -qiE '<svg|<\?xml'; }
is_png()  { file -b "$1" 2>/dev/null | grep -qi 'PNG image'; }
bytes()   { wc -c < "$1" 2>/dev/null || echo 0; }
big_svg() { [ "$(bytes "$1")" -gt 200 ]; }   # icon SVGs are tiny (~600B)
big_png() { [ "$(bytes "$1")" -gt 1024 ]; }  # reject placeholder/blank PNGs

# 1) simple-icons (SVG) — CDN, with raw-GitHub fallback for the same slug
svg="$outdir/$slug.svg"
if curl -fsSL -A "$ua" "https://cdn.simpleicons.org/$slug" -o "$svg" 2>/dev/null && is_svg "$svg" && big_svg "$svg"; then
  ok "simple-icons SVG (monochrome, tint-ready) -> $svg"; exit 0
fi
if curl -fsSL -A "$ua" "https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/$slug.svg" -o "$svg" 2>/dev/null && is_svg "$svg" && big_svg "$svg"; then
  ok "simple-icons SVG via raw GitHub (monochrome, tint-ready) -> $svg"; exit 0
fi
rm -f "$svg"; no "simple-icons: no match for slug '$slug'"

# 2) clearbit (PNG, needs domain)
if [ -n "$domain" ]; then
  png="$outdir/$slug.png"
  if curl -fsSL -A "$ua" "https://logo.clearbit.com/$domain?size=256" -o "$png" 2>/dev/null && is_png "$png" && big_png "$png"; then
    ok "clearbit PNG (full-color) -> $png"; exit 0
  fi
  rm -f "$png"; no "clearbit: no logo for '$domain'"
fi

# 3) favicon (last resort, low quality)
if [ -n "$domain" ]; then
  png="$outdir/$slug.png"
  if curl -fsSL -A "$ua" "https://www.google.com/s2/favicons?domain=$domain&sz=128" -o "$png" 2>/dev/null && is_png "$png" && big_png "$png"; then
    ok "favicon PNG (LOW QUALITY — prefer Wikimedia/Brandfetch) -> $png"; exit 0
  fi
  rm -f "$png"; no "favicon: nothing usable for '$domain'"
fi

cat >&2 <<EOF
✗ No automatic hit for '$slug'${domain:+ / $domain}.
  Try by hand (best for full wordmark logos):
   • Wikimedia: search Commons "<Company> logo", grab the Original .svg, curl -L it
   • Brandfetch: https://cdn.brandfetch.io/<domain>/w/512/h/512
   • Press kit: WebSearch "<Company> brand assets / logo svg"
EOF
exit 1
