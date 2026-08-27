# Documentation

This directory contains the Sphinx infrastructure used to build the project
documentation.

- Sphinx configuration and build glue (`Makefile`, `conf.py`,
  `requirements.txt`) and the top-level `index.rst` live directly under
  `marvell-docs/`.
- SONiC-specific content is authored in Markdown and lives under
  [`marvell-docs/SONIC/`](SONIC/index.md).

## Prerequisites

- Python 3.9+
- `make`

## Generating the docs

```sh
# 1. Create and activate a virtual environment (one-time setup)
python3 -m venv .venv
. .venv/bin/activate

# 2. Install the pinned doc-build dependencies
pip install -r marvell-docs/requirements.txt

# 3. Build the HTML docs
make -C marvell-docs html
```

If you'd rather not create a venv, any environment with the packages from
`marvell-docs/requirements.txt` installed will work.

## Viewing the output

The generated HTML is written to `marvell-docs/_build/html/`. Open it directly, or
serve it locally:

```sh
python3 -m http.server -d marvell-docs/_build/html 8000
```

Then browse to <http://localhost:8000>.

## Cleaning build artifacts

```sh
make -C marvell-docs clean
```

## Adding content

Each top-level section is a **folder with an `index.md`** inside
`marvell-docs/SONIC/` (e.g. `marvell-docs/SONIC/getting-started/index.md`). To add a new
top-level section:

1. Create `marvell-docs/SONIC/my-section/index.md`.
2. Reference it from the `{toctree}` in [`marvell-docs/index.rst`](index.rst), for
   example:

   ```rst
   .. toctree::
      :maxdepth: 1
      :hidden:
      :caption: Sections

      About Prestera SONiC <SONIC/about/index>
      Getting Started <SONIC/getting-started/index>
      My Section <SONIC/my-section/index>
   ```

3. Add a matching card to the landing-page grid in `marvell-docs/index.rst` if it
   should appear on the front page.

To add a sub-page within an existing section, drop another `.md` file next
to that section's `index.md` and reference it from a `{toctree}` inside
that section's `index.md`.

### Adding images

- **Page-specific images** (diagrams, screenshots): put them in a single
  `images/` subfolder at the **top-level heading folder** (e.g.
  `marvell-docs/SONIC/about/images/diagram.png`) — never inside a nested sub-page's
  own folder. Reference them with a relative path from wherever the page
  lives, e.g. `![alt text](images/diagram.png)` from a page directly under
  `about/`, or `![alt text](../images/diagram.png)` from a page one level
  deeper (e.g. `about/releases/`).
- **Shared/site-wide images** (logo, favicon, icons reused across pages):
  put them under `marvell-docs/_static/images/` (e.g.
  `marvell-docs/_static/images/marvell_sonic_logo.png`) and reference them with a
  path rooted at `_static/`, e.g. `![alt text](/_static/images/foo.png)`
  or via `html_logo` / `html_favicon` in `conf.py`.

## Layout

```
marvell-docs/
├── conf.py                     Sphinx configuration
├── index.rst                   Top-level landing page
├── Makefile                    `make html` / `make clean` targets
├── requirements.txt            Pinned Python dependencies for the doc build
├── _static/                    Static assets (CSS, JS)
│   ├── css/                    Custom stylesheet(s)
│   └── images/                 Shared/site-wide images (logo, favicon, ...)
├── _templates/                 Custom HTML templates
└── SONIC/                      SONiC-specific content, authored in Markdown
    ├── about/                    About
    │   ├── index.md
    │   ├── what-is-sonic.md
    │   ├── why-marvell-sonic.md
    │   └── images/
    │       ├── sonic_architecture.svg
    │       └── release-naming-convention.svg
    ├── getting-started/           Getting Started
    │   ├── index.md
    │   ├── marvell-prestera/
    │   │   └── index.md
    │   ├── build/
    │   │   └── index.md
    │   ├── deploy-sonic-on-marvell-prestera/
    │   │   └── index.md
    │   └── images/
    │       └── prestera-soc-naming.svg
    ├── developers/                For Developers
    │   ├── index.md
    │   ├── know-marvell-sonic-repositories.md
    │   └── whitemodel-development/
    │       ├── index.md
    │       └── sonic-virtual-switch/
    │           └── index.md
    ├── releases/                  Releases
    │   ├── index.md
    │   ├── details.md
    │   └── rls-01.202511.01.md
    └── collaborate/               Collaborate
        ├── index.md
        ├── how-to-contribute.md
        └── raise-issues.md
```

## AI Agent Guidelines

Conventions established for this docs site (folder structure, naming,
styling, build/verify workflow, etc.) are captured in a Cursor rule at
[`.cursor/rules/sonic-docs.mdc`](../.cursor/rules/sonic-docs.mdc), scoped to
`marvell-docs/**`. It's automatically surfaced to Cursor/AI agents working on files
under `marvell-docs/`, so future additions stay consistent instead of re-deciding
(or drifting from) decisions already made here.

To add to it (e.g. after establishing a new convention):

1. Open `.cursor/rules/sonic-docs.mdc`.
2. Add a concise, actionable bullet under the relevant section (or add a new
   `##` section if it's a new category of convention).
3. Keep it short — this is a quick-reference for an agent, not a full guide;
   link out to this README or other docs for longer explanations.

To create an additional, differently-scoped rule (e.g. one that applies
outside `marvell-docs/`), see the general
[Cursor rules docs](https://cursor.com/docs/context/rules) or ask an agent to
create one for you.

## Publishing to GitHub Pages

[`.github/workflows/docs.yml`](../.github/workflows/docs.yml) builds the docs
on every push/PR touching `marvell-docs/**`, and deploys the result to GitHub Pages
on pushes to `main`.

One-time repo setup required: in **Settings → Pages**, set **Source** to
**GitHub Actions**. After that, the site is published automatically at
`https://<org>.github.io/<repo>/` whenever `main` is updated.
