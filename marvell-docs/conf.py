# Configuration file for the Sphinx documentation builder.
# See https://www.sphinx-doc.org/en/master/usage/configuration.html

from datetime import datetime

project = "Prestera SONiC"
author = "Marvell"
copyright = f"2024-{datetime.now().year}, Marvell"

# Current documentation version, shown/selected in the release drop-down
# (version switcher) in the navbar. Must match one of the "version" keys
# in _static/versions.json.
version = "master"

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
]

myst_heading_anchors = 3

templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "README.md",
    ".venv",
    "venv",
]

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]
html_js_files = ["js/navbar-dropdown.js"]
html_show_sourcelink = False

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
    # A single, fixed URL (not per-version-relative) so every deployed
    # version's dropdown fetches the exact same, always-up-to-date version
    # list, rather than each version serving its own possibly-stale copy.
    # This is deployed by the docs workflow at the site root, alongside the
    # per-version subfolders (master/, etc.) -- see .github/workflows/docs.yml.
    "switcher": {
        "json_url": "https://marvellembeddedprocessors.github.io/marvell-sonic-buildimage/versions.json",
        "version_match": version,
    },
    "icon_links": [
        {
            "name": "GitHub Repo",
            "url": "https://github.com/MarvellEmbeddedProcessors/marvell-sonic-buildimage",
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        },
    ],
    "show_toc_level": 2,
    "navigation_depth": 4,
    "footer_start": ["copyright"],
    "footer_end": [],
}
