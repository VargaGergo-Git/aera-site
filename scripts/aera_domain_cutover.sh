#!/bin/bash
# Move aera-site from the GitHub Pages URL to a real domain, in one command.
#
# PARKED as of 2026-09-20. Gergo decided against buying a domain for now: the
# shipped 3.0 problems matter more than the website, and the site stays on
# https://vargagergo-git.github.io/aera-site/. Nothing runs this, nothing waits
# on it, and nobody should be asked about a domain again. It is kept because it
# is written and tested and the reasoning below did not stop being true; only
# the priority changed.
#
# Why this is a script and not a checklist: the old URL is written into 31 files
# as an ABSOLUTE url, in canonical tags, og:url, JSON-LD, the sitemap, the notes
# feed, robots.txt and the IndexNow workflow. Doing that by hand is an afternoon,
# and the failure mode is silent: one stale canonical tells Google the real page
# lives somewhere else and the note stops being indexable. So the move is
# mechanical, and the script refuses to finish if a single old URL survives.
#
#   ./scripts/aera_domain_cutover.sh aera.app
#   ./scripts/aera_domain_cutover.sh aera.app --dry-run
#   ./scripts/aera_domain_cutover.sh aera.app --gsc-token googleXXXXXXXX
#
# It changes files only. It never commits, never pushes, and never touches DNS or
# the registrar; it prints exactly what to type where, at the end.

set -euo pipefail

OLD_HOST="vargagergo-git.github.io"
OLD_BASE="https://vargagergo-git.github.io/aera-site"
INDEXNOW_KEY="09571b31bc62e1964a5643dfb26caff4"

# GitHub Pages apex IPv4, from docs.github.com "Managing a custom domain".
PAGES_A=(185.199.108.153 185.199.109.153 185.199.110.153 185.199.111.153)
PAGES_AAAA=(2606:50c0:8000::153 2606:50c0:8001::153 2606:50c0:8002::153 2606:50c0:8003::153)

DOMAIN=""
GSC_TOKEN=""
DRY_RUN=0

usage() {
  cat >&2 <<USAGE
usage: $0 <domain> [--dry-run] [--gsc-token <google-site-verification-token>]

  <domain>       the bare domain you bought, e.g. aera.app  (or www.aera.app)
  --dry-run      show every file that would change, write nothing
  --gsc-token    also drop the Google Search Console HTML verification file
USAGE
  exit 2
}

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    --gsc-token) GSC_TOKEN="${2:-}"; [ -n "$GSC_TOKEN" ] || usage; shift 2 ;;
    -h|--help) usage ;;
    -*) echo "unknown flag: $1" >&2; usage ;;
    *) [ -z "$DOMAIN" ] || usage; DOMAIN="$1"; shift ;;
  esac
done

[ -n "$DOMAIN" ] || usage

# A domain, not a URL and not a path. Catch the paste of "https://aera.app/" early.
if ! printf '%s' "$DOMAIN" | grep -qE '^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)+$'; then
  echo "error: '$DOMAIN' is not a bare domain. Pass aera.app, not https://aera.app/" >&2
  exit 1
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

[ -f index.html ] && [ -f sitemap.xml ] || {
  echo "error: $ROOT does not look like the aera-site repo (no index.html/sitemap.xml)" >&2
  exit 1
}

NEW_BASE="https://$DOMAIN"

# Anything with a URL in it. Binary assets and .git are never touched.
mapfile -t FILES < <(
  grep -rlF "$OLD_HOST" . \
    --include='*.html' --include='*.xml' --include='*.txt' --include='*.md' \
    --include='*.css' --include='*.js' --include='*.json' --include='*.yml' --include='*.yaml' \
    --exclude-dir=.git 2>/dev/null | sort
)

if [ "${#FILES[@]}" -eq 0 ]; then
  echo "Nothing to rewrite: no file mentions $OLD_HOST."
  echo "The site may already be on a domain. Check CNAME:"
  [ -f CNAME ] && cat CNAME
  exit 0
fi

echo "Moving $OLD_BASE  ->  $NEW_BASE"
echo "${#FILES[@]} files carry the old URL:"
for f in "${FILES[@]}"; do
  n=$(grep -cF "$OLD_HOST" "$f")
  printf '  %4d  %s\n' "$n" "${f#./}"
done
echo

if [ "$DRY_RUN" -eq 1 ]; then
  echo "--dry-run: nothing written."
  exit 0
fi

# Order matters. The long form carries the /aera-site path prefix, which the
# custom domain drops; rewriting the bare host first would leave /aera-site
# glued onto the new domain and every URL would 404.
for f in "${FILES[@]}"; do
  perl -pi -e "s{\Qhttps://$OLD_HOST/aera-site\E}{$NEW_BASE}g" "$f"
  perl -pi -e "s{\Qhttps://$OLD_HOST\E}{$NEW_BASE}g" "$f"
  perl -pi -e "s{\Q$OLD_HOST\E}{$DOMAIN}g" "$f"
  # The path prefix survives the host rewrite wherever the URL was assembled from
  # parts rather than written whole: the IndexNow workflow builds its keyLocation
  # as "https://$HOST/aera-site/$KEY.txt", where no line ever contains the host
  # literally. A host-only rewrite leaves /aera-site glued to the new domain and
  # the key 404s, which fails ownership silently. Found by running this script.
  perl -pi -e "s{\Q$DOMAIN\E/aera-site}{$DOMAIN}g" "$f"
  perl -pi -e 's{\$HOST/aera-site}{\$HOST}g' "$f"
done

# GitHub Pages reads CNAME on every build; without it the custom domain setting
# is dropped the next time the branch is pushed.
printf '%s\n' "$DOMAIN" > CNAME
echo "wrote CNAME -> $DOMAIN"

# IndexNow proves ownership by serving the key at the host root. On the old URL
# the key sat under /aera-site/; on a domain it must be at /.
if [ -f "$INDEXNOW_KEY.txt" ]; then
  echo "IndexNow key file already at root: $INDEXNOW_KEY.txt"
else
  printf '%s\n' "$INDEXNOW_KEY" > "$INDEXNOW_KEY.txt"
  echo "wrote $INDEXNOW_KEY.txt"
fi

if [ -n "$GSC_TOKEN" ]; then
  TOKEN_FILE="${GSC_TOKEN%.html}.html"
  printf 'google-site-verification: %s\n' "$TOKEN_FILE" > "$TOKEN_FILE"
  echo "wrote $TOKEN_FILE (Search Console HTML file method)"
fi

# The whole point of the script: prove the move is complete.
LEFTOVER=$(grep -rlE "$OLD_HOST|/aera-site/" . --exclude-dir=.git 2>/dev/null | grep -v '^\./scripts/aera_domain_cutover\.sh$' || true)
if [ -n "$LEFTOVER" ]; then
  echo >&2
  echo "INCOMPLETE: these files still carry the old host or the /aera-site/ path" >&2
  printf '  %s\n' $LEFTOVER >&2
  exit 1
fi

cat <<NEXT

Files are done and the tree is clean of the old URL. Nothing is committed.

What only you can do now, in this order:

1. Registrar DNS for $DOMAIN
NEXT

if printf '%s' "$DOMAIN" | grep -q '^www\.'; then
  cat <<NEXT
   One record:
     CNAME   www   ->  ${OLD_HOST}.
NEXT
else
  echo "   Four A records on the apex (@):"
  for ip in "${PAGES_A[@]}"; do echo "     A     @     -> $ip"; done
  echo "   And, for IPv6:"
  for ip in "${PAGES_AAAA[@]}"; do echo "     AAAA  @     -> $ip"; done
  echo "   Plus, so www works too:"
  echo "     CNAME www   -> ${OLD_HOST}."
fi

cat <<NEXT

2. GitHub: repo Settings > Pages > Custom domain = $DOMAIN > Save,
   then tick "Enforce HTTPS" once the certificate is issued (up to an hour).

3. Nothing else. GitHub Pages 301-redirects $OLD_BASE/* to the new domain by
   itself once the custom domain is live, so existing links and whatever Bing
   has indexed keep working and pass their value on.

Worth knowing: until this lands, the logo in the top bar links to "/", which on
the old URL is vargagergo-git.github.io and not this site at all. The move fixes
that without a code change.
NEXT
