#!/usr/bin/env bash
#
# Build the multi-version documentation site locally, the same way the "Docs"
# GitHub Actions workflow (.github/workflows/docs.yml) assembles it for GitHub
# Pages. It builds:
#
#   * the default branch, marked "(latest)" and used for the root redirect, and
#   * every "rls-*" tag,
#
# each into <site>/<version>/ (version = the ref name with the "rls-" prefix
# stripped, else "master" -- matching conf.py), then generates versions.json for
# the switcher and a root index.html that redirects to the default version.
#
# Differences from CI (by design):
#   * Refs are checked out into throwaway `git worktree`s, so your current
#     working tree is left untouched. Only COMMITTED state is built -- commit
#     (and tag) to preview a release. To preview uncommitted edits to the branch
#     you're on, use `make -C marvell-docs html` instead.
#   * The Pages base URL defaults to a local one (for `--serve`); CI resolves the
#     repo's real Pages URL via actions/configure-pages.
#
# Usage:
#   marvell-docs/_scripts/build-site.sh [options]
#
# Options:
#   --output DIR         Output site directory (default: marvell-docs/_build/site)
#   --base URL           Pages base URL baked into versions.json / the switcher
#                        (default: http://localhost:PORT)
#   --serve              Serve the assembled site over HTTP after building
#   --port PORT          Port for --base/--serve (default: 8000)
#   --default-branch REF Ref treated as the default/"latest" version
#                        (default: the currently checked-out branch)
#   --venv               Create/reuse marvell-docs/_build/.venv and install
#                        requirements.txt into it (otherwise deps must be on PATH)
#   -h, --help           Show this help
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(git -C "$DOCS_DIR" rev-parse --show-toplevel)"

SITE="$DOCS_DIR/_build/site"
PORT=8000
BASE=""
SERVE=0
USE_VENV=0
DEFAULT_BRANCH="$(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD)"

usage() { sed -n '2,45p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; }

while [ $# -gt 0 ]; do
  case "$1" in
    --output)         SITE="$2"; shift 2 ;;
    --base)           BASE="$2"; shift 2 ;;
    --serve)          SERVE=1; shift ;;
    --port)           PORT="$2"; shift 2 ;;
    --default-branch) DEFAULT_BRANCH="$2"; shift 2 ;;
    --venv)           USE_VENV=1; shift ;;
    -h|--help)        usage; exit 0 ;;
    *) echo "error: unknown argument '$1'" >&2; usage >&2; exit 2 ;;
  esac
done

: "${BASE:=http://localhost:$PORT}"
BASE="${BASE%/}"

if [ "$DEFAULT_BRANCH" = "HEAD" ]; then
  echo "error: detached HEAD; pass --default-branch <ref>" >&2
  exit 2
fi

# version string for a ref name (mirrors conf.py: strip "rls-", else "master").
ref_version() {
  case "$1" in
    rls-*) printf '%s' "${1#rls-}" ;;
    *)     printf 'master' ;;
  esac
}

# Optional self-contained venv (mirrors CI's `pip install -r requirements.txt`).
if [ "$USE_VENV" = 1 ]; then
  VENV="$DOCS_DIR/_build/.venv"
  echo "==> Setting up venv at $VENV"
  python3 -m venv "$VENV"
  # shellcheck disable=SC1091
  . "$VENV/bin/activate"
  pip install --quiet --upgrade pip
  pip install --quiet -r "$DOCS_DIR/requirements.txt"
fi

if ! command -v sphinx-build >/dev/null 2>&1; then
  echo "error: sphinx-build not found on PATH." >&2
  echo "       Install deps (pip install -r marvell-docs/requirements.txt) or pass --venv." >&2
  exit 1
fi

WORKTREE_BASE="$(mktemp -d)"
cleanup() {
  # Remove any worktrees we added, then their scratch parent.
  if [ -d "$WORKTREE_BASE" ]; then
    for wt in "$WORKTREE_BASE"/*; do
      [ -d "$wt" ] && git -C "$REPO_ROOT" worktree remove --force "$wt" 2>/dev/null || true
    done
    rm -rf "$WORKTREE_BASE"
  fi
  git -C "$REPO_ROOT" worktree prune 2>/dev/null || true
}
trap cleanup EXIT

rm -rf "$SITE"
mkdir -p "$SITE"

# Build one ref (checked out into a detached worktree) into $SITE/<version>/.
#   $1 = git ref to check out   $2 = ref name passed to conf.py via GITHUB_REF_NAME
build_ref() {
  local checkout_ref="$1" name="$2"
  local v; v="$(ref_version "$name")"
  local wt="$WORKTREE_BASE/wt-$v"

  echo "==> Building '$name' as version '$v'"
  if ! git -C "$REPO_ROOT" rev-parse -q --verify "${checkout_ref}^{commit}" >/dev/null; then
    echo "    skip: ref '$checkout_ref' not found"
    return 0
  fi
  git -C "$REPO_ROOT" worktree add --quiet --detach "$wt" "$checkout_ref"

  if [ ! -f "$wt/marvell-docs/Makefile" ]; then
    echo "    skip: no marvell-docs/ at '$name'"
    git -C "$REPO_ROOT" worktree remove --force "$wt"
    return 0
  fi

  GITHUB_REF_NAME="$name" DOCS_SWITCHER_JSON_URL="$BASE/versions.json" \
    make -C "$wt/marvell-docs" html

  rm -rf "${SITE:?}/$v"
  mkdir -p "$SITE/$v"
  cp -R "$wt/marvell-docs/_build/html/." "$SITE/$v/"
  rm -rf "$SITE/$v/.doctrees"

  git -C "$REPO_ROOT" worktree remove --force "$wt"
  echo "    done: /$v/"
}

# Default branch first (the "latest" version), then every rls-* tag.
build_ref "$DEFAULT_BRANCH" "$DEFAULT_BRANCH"
while read -r tag; do
  [ -n "$tag" ] || continue
  build_ref "$tag" "$tag"
done < <(git -C "$REPO_ROOT" tag -l 'rls-*')

if [ -z "$(ls -A "$SITE")" ]; then
  echo "error: no versions were built" >&2
  exit 1
fi

default_version="$(ref_version "$DEFAULT_BRANCH")"

# Switcher list + root redirect (same tooling the workflow uses).
python3 "$DOCS_DIR/_scripts/gen_versions_json.py" "$SITE" "$default_version" "$BASE"

cat > "$SITE/index.html" <<HTML
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url=./$default_version/">
    <link rel="canonical" href="./$default_version/">
    <title>Prestera SONiC Documentation</title>
  </head>
  <body>
    Redirecting to <a href="./$default_version/">./$default_version/</a>&hellip;
  </body>
</html>
HTML

echo
echo "==> Site assembled at: $SITE"
echo "    versions: $(cd "$SITE" && ls -d */ 2>/dev/null | tr -d /  | tr '\n' ' ')"

if [ "$SERVE" = 1 ]; then
  echo "==> Serving at http://localhost:$PORT/  (Ctrl-C to stop)"
  exec python3 -m http.server "$PORT" --directory "$SITE"
fi
