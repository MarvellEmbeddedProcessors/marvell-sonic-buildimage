# Configuration file for the Sphinx documentation builder.
# See https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import re
import sys
from datetime import datetime

# Make the dev/build helpers under _scripts/ importable (e.g. the generator for
# the release-naming SVG, which is rebuilt at build time -- see setup() below).
_CONFDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_CONFDIR, "_scripts"))

# Repo being built (set in CI), falling back to the public repo for local
# builds. Drives both the GitHub icon link and the version-switcher URL below.
_github_server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
_github_repo = os.environ.get(
    "GITHUB_REPOSITORY", "MarvellEmbeddedProcessors/marvell-sonic-buildimage"
)
_repo_url = f"{_github_server}/{_github_repo}"

# GitHub Pages site for that repo (https://<owner>.github.io/<repo>), used as
# the switcher's base for LOCAL builds. In CI the workflow overrides this with
# the repo's *real* Pages URL via DOCS_SWITCHER_JSON_URL (resolved from the
# GitHub API, so it also covers Enterprise and custom-domain hosts) -- see
# .github/workflows/docs.yml.
_owner, _, _repo_name = _github_repo.partition("/")
_pages_base = f"https://{_owner.lower()}.github.io/{_repo_name}"

project = "Prestera SONiC"
author = "Marvell"
copyright = f"2024-{datetime.now().year}, Marvell"

# Documentation version: the deploy subfolder and the entry selected in the
# release drop-down (version switcher). Derived from the ref being built by
# stripping the "rls-" prefix from its name; refs not named "rls-*" (feature
# branches, a non-"rls-" default branch, local builds) are "master". The naming
# intentionally differs between branches and tags:
#   * branch "rls-202511.01"     -> version "202511.01"
#   * tag    "rls-01.202511.01"  -> version "01.202511.01"
# The default branch and release tags are the refs that get published (see
# .github/workflows/docs.yml). This becomes an entry in the version switcher's
# list, which the workflow regenerates on every deploy from the folders present
# on gh-pages -- so there is no hand-maintained version file to keep in sync.
_ref_name = os.environ.get("GITHUB_REF_NAME", "")
version = _ref_name[len("rls-"):] if _ref_name.startswith("rls-") else "master"

# Release tag shown on the release-notes page and naming diagram. Derived (not
# hard-coded) from the ref, so the same source renders whatever the current ref
# is named: the tag "rls-01.202511.01" for a release, or the branch
# "rls-202511.01" otherwise. Exposed to Markdown via a {{ release_tag }}
# substitution and to templates via html_context, so no version string is baked
# into the content.
release = version
release_tag = f"rls-{version}"

# Is this build from a *release tag* (vs a branch / local build)? A release tag
# yields a 3-part version ("01.202511.01"); a branch yields 2 parts
# ("202511.01") and everything else is "master". Only release tags get a
# release-notes entry (branches are in-development, not a release): the
# release-notes toctree entry is generated in setup() only when this is true
# (so it's absent from the section nav on branch builds), and the navbar drops
# it too (via html_context) -- see _templates/navbar-nav.html.
is_release = bool(re.fullmatch(r"\d+\.\d+\.\d+", version))

html_title = ""
html_logo = "_static/images/marvell_sonic_logo.png"
html_favicon = "_static/images/tab_logo.svg"

root_doc = "index"

extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
]

# Allow both .rst and Markdown (.md) sources. SONiC-specific content lives
# under SONIC/ and is authored in Markdown.
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "substitution",
]

# Values usable as {{ ... }} substitutions in Markdown pages.
myst_substitutions = {
    "release_tag": release_tag,
    "release_version": version,
}

myst_heading_anchors = 3

templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "_scripts",
    "Thumbs.db",
    ".DS_Store",
    "README.md",
    ".venv",
    "venv",
    # Generated at build time and pulled into details.md via {include}; not a
    # standalone document (see setup() below and _scripts/gen_releases_table.py).
    "SONIC/releases/_releases_table.md",
    # Likewise generated in setup(): the (conditional) release-notes toctree
    # entry, pulled into SONIC/releases/index.md via {include}.
    "SONIC/releases/_release_notes_toctree.md",
]

# On branch/local builds there is no release, so the release-notes page is not
# built at all (its toctree entry is omitted -- see setup()). Excluding it keeps
# it out of the section nav without leaving an orphan page.
if not is_release:
    exclude_patterns.append("SONIC/releases/release-notes.md")

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]
html_js_files = ["js/navbar-dropdown.js"]
html_show_sourcelink = False

# Expose the derived release tag and the release/non-release flag to custom
# templates (the navbar drops the release-notes entry on non-release builds).
html_context = {"release_tag": release_tag, "is_release": is_release}

# Remove sidebar on the card-based landing page.
html_sidebars = {"index": []}

# Only show a small search icon (no fake search-bar) in the navbar.
html_theme_options = {
    "navbar_persistent": [],
    "navbar_end": [
        "version-switcher",
        "search-button",
        "theme-switcher",
        "navbar-icon-links",
    ],
    # Version list URL. In CI the workflow sets DOCS_SWITCHER_JSON_URL to the
    # repo's real Pages URL (works on github.com, Enterprise, and custom-domain
    # hosts, including GitHub's randomized *.pages.github.io domains for private
    # repos); locally it falls back to the conventional <owner>.github.io URL
    # above. Either way each repo/mirror serves and reads its OWN list at its
    # site root, which the workflow regenerates on every deploy (see
    # _scripts/gen_versions_json.py).
    "switcher": {
        "json_url": os.environ.get(
            "DOCS_SWITCHER_JSON_URL", f"{_pages_base}/versions.json"
        ),
        "version_match": version,
    },
    # Never fetch/validate json_url at build time: the switcher list only needs
    # to resolve at runtime in the browser (after deploy). The build-time check
    # is fatal when the URL returns a non-JSON 200 body -- which happens before
    # the first deploy on GitHub's randomized *.pages.github.io Pages domains --
    # so we disable it and let the switcher populate client-side instead.
    "check_switcher": False,
    "icon_links": [
        {
            "name": "GitHub Repo",
            "url": _repo_url,
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        },
    ],
    "show_toc_level": 2,
    "navigation_depth": 4,
    "footer_start": ["copyright"],
    "footer_end": [],
}


def setup(app):
    """Regenerate derived assets at build time.

    Both assets are git-ignored and rebuilt here before the docs are read:

    * The release-naming diagram is rendered from the (branch-derived) `version`
      so the same synced source produces the correct convention in each repo.
    * The Releases > Details table is generated from the repo's release tags
      (see _scripts/gen_releases_table.py) and pulled into details.md via
      {include}, so it lists every release without a hand-maintained table.
    """
    from gen_release_naming_svg import render as render_naming_svg
    from gen_releases_table import render as render_releases_table

    render_naming_svg(
        version,
        out_path=os.path.join(
            _CONFDIR, "SONIC", "about", "images", "release-naming-convention.svg"
        ),
    )
    render_releases_table(
        os.path.join(_CONFDIR, "SONIC", "releases", "_releases_table.md")
    )

    # Conditional release-notes toctree entry, pulled into
    # SONIC/releases/index.md via {include}. Emitted only for release-tag builds
    # so the section nav lists a release-notes page only for actual releases
    # (branch builds have no release, so the include is empty).
    toctree_inc = os.path.join(
        _CONFDIR, "SONIC", "releases", "_release_notes_toctree.md"
    )
    with open(toctree_inc, "w", encoding="utf-8") as f:
        if is_release:
            f.write("```{toctree}\n:maxdepth: 1\n\nrelease-notes\n```\n")
        else:
            f.write("% No release-notes entry: this is not a release-tag build.\n")

    return {"parallel_read_safe": True, "parallel_write_safe": True}
