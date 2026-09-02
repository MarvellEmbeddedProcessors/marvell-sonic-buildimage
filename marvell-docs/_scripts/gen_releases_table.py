#!/usr/bin/env python3
"""Generate the "Releases > Details" table listing *all* release tags.

The Details page (``SONIC/releases/details.md``) shows one row per Prestera
SONiC release. The list of releases is auto-discovered from the repo's git tags
(any tag named ``rls-<major>.<sonic>.<minor>``, e.g. ``rls-01.202511.01``) so it
stays in sync automatically as new releases are tagged -- there is no
hand-maintained list of which releases exist.

A tag name only carries the tag and (derivably) its release branch, so the
remaining columns (SAI versions, date, lifecycle) come from a small committed
map keyed by tag: ``SONIC/releases/releases.yaml``. A tag with no entry there
still appears, with "TBD" for those columns.

Each release's tag links to *that release's own* deployed notes. On the
multi-version site every version lives under ``<site>/<version>/`` (see
.github/workflows/docs.yml), so from this page
(``<version>/SONIC/releases/details.html``) another release's notes are three
levels up and back down: ``../../../<other-version>/SONIC/releases/
release-notes.html``. The current build's own release links to the local
``release-notes.html`` instead (works for local single-version previews too).

The rendered table is written as a MyST fragment that ``details.md`` includes;
it is git-ignored and regenerated on every build via a ``setup()`` hook in
``conf.py``. To produce it manually:

    python marvell-docs/_scripts/gen_releases_table.py /tmp/table.md
    DOCS_RELEASE_TAGS="rls-01.202511.01 rls-02.202511.01" \\
        python marvell-docs/_scripts/gen_releases_table.py /tmp/table.md
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

_RELEASES_DIR = Path(__file__).resolve().parents[1] / "SONIC/releases"
_META_FILE = _RELEASES_DIR / "releases.yaml"
_OUT = _RELEASES_DIR / "_releases_table.md"

# A release *tag* is the 3-part form rls-<major>.<sonic>.<minor>; the 2-part
# form (rls-<sonic>.<minor>) is a release *branch* and is not itself a release.
_TAG_RE = re.compile(r"^rls-\d+\.\d+\.\d+$")

_COLUMNS = [
    "Release Tag",
    "Release Branch",
    "Marvell SAI Version",
    "OCP SAI Version",
    "Release Date",
    "Lifecycle",
    "URL",
]


def _repo_url() -> str:
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repo = os.environ.get(
        "GITHUB_REPOSITORY", "MarvellEmbeddedProcessors/marvell-sonic-buildimage"
    )
    return f"{server}/{repo}"


def _current_version() -> str:
    """Version of the ref being built (matches conf.py's derivation)."""
    ref = os.environ.get("GITHUB_REF_NAME", "")
    return ref[len("rls-"):] if ref.startswith("rls-") else "master"


def _git_tags() -> list[str]:
    try:
        out = subprocess.check_output(
            ["git", "tag", "-l", "rls-*"],
            cwd=str(_RELEASES_DIR),
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]


def _load_meta() -> dict:
    """Load the per-release metadata map. Returns {} if unavailable."""
    if not _META_FILE.is_file():
        return {}
    try:
        import yaml
    except ImportError:
        return {}
    data = yaml.safe_load(_META_FILE.read_text(encoding="utf-8")) or {}
    return data.get("releases", {}) or {}


def _discover_tags(meta: dict) -> list[str]:
    """Release tags to list: git tags + metadata keys (env override wins).

    Unioning the metadata keys means a known release still shows up in local
    previews where its tag may not be checked out, while git tags pick up newly
    cut releases automatically.
    """
    env = os.environ.get("DOCS_RELEASE_TAGS")
    if env is not None:
        candidates = env.split()
    else:
        candidates = [*_git_tags(), *meta.keys()]
    tags = {t for t in candidates if _TAG_RE.match(t)}
    # Newest first, by numeric (major, sonic, minor).
    return sorted(tags, key=lambda t: _version_key(t[len("rls-"):]), reverse=True)


def _version_key(version: str) -> tuple[int, ...]:
    return tuple(int(p) for p in version.split("."))


def _branch_of(version: str) -> str:
    """Release branch for a tag version: rls-<sonic>.<minor>."""
    _major, sonic, minor = version.split(".")
    return f"rls-{sonic}.{minor}"


def _notes_href(version: str, current_version: str) -> str:
    if version == current_version:
        return "release-notes.html"
    # Sibling version folder at the site root (see module docstring).
    return f"../../../{version}/SONIC/releases/release-notes.html"


def _ext_link(href: str, text: str, *, title: str | None = None) -> str:
    title_attr = f' title="{title}"' if title else ""
    return (
        f'<a class="reference external" href="{href}"{title_attr} '
        f'target="_blank" rel="noopener">{text}</a>'
    )


def _github_cell(repo_url: str, branch: str) -> str:
    href = f"{repo_url}/tree/{branch}"
    return (
        f'<a class="reference external" href="{href}" '
        f'title="View on GitHub" target="_blank" rel="noopener">'
        f'<i class="fa-brands fa-github fa-lg" aria-hidden="true"></i>'
        f'<span class="visually-hidden">View {branch} on GitHub</span></a>'
    )


def _row(tag: str, meta: dict, current_version: str, repo_url: str) -> str:
    version = tag[len("rls-"):]
    branch = _branch_of(version)
    info = meta.get(tag, {})

    tag_cell = f'<a class="reference internal" href="{_notes_href(version, current_version)}">{tag}</a>'
    marvell_sai = info.get("marvell_sai", "TBD")
    ocp_label = info.get("ocp_sai")
    ocp_url = info.get("ocp_sai_url")
    if ocp_label and ocp_url:
        ocp_cell = _ext_link(ocp_url, ocp_label)
    else:
        ocp_cell = ocp_label or "TBD"
    release_date = info.get("release_date", "TBD")
    lifecycle = info.get("lifecycle", "TBD")

    cells = [
        tag_cell,
        branch,
        marvell_sai,
        ocp_cell,
        release_date,
        lifecycle,
        _github_cell(repo_url, branch),
    ]
    return "| " + " | ".join(cells) + " |"


def render(out_path: Path | str = _OUT) -> Path:
    """Render the releases table fragment and write it to ``out_path``."""
    out_path = Path(out_path)
    meta = _load_meta()
    tags = _discover_tags(meta)
    current_version = _current_version()
    repo_url = _repo_url()

    header = "| " + " | ".join(_COLUMNS) + " |"
    separator = "|" + "|".join(["---"] * len(_COLUMNS)) + "|"
    if tags:
        rows = [_row(t, meta, current_version, repo_url) for t in tags]
    else:
        # Keep a valid (empty) table so the include never breaks the build.
        rows = ["| " + " | ".join(["_None yet._"] + [""] * (len(_COLUMNS) - 1)) + " |"]

    lines = [
        "<!-- Generated by _scripts/gen_releases_table.py -- do not edit. -->",
        ":::{table}",
        ":class: table releases-table",
        "",
        header,
        separator,
        *rows,
        ":::",
        "",
    ]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


if __name__ == "__main__":
    dest = sys.argv[1] if len(sys.argv) > 1 else _OUT
    print(render(dest))
