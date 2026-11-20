# Documentation

This directory contains the Sphinx infrastructure used to build the project
documentation.

- Sphinx configuration and build glue (`Makefile`, `conf.py`,
  `requirements.txt`) and the top-level `index.rst` live directly under
  `marvell-docs/`.
- SONiC-specific content is authored in Markdown and lives under
  [`marvell-docs/SONIC/`](SONIC/index.md).

## Prerequisites

- Python 3.12 (matches CI; 3.9+ may work for local builds)
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

## Design

### Build modes

There are two build modes:

1. **Single-version** — `make -C marvell-docs html` (or the Docs workflow *validate*
   job on every push). Sphinx reads the **current checkout** and writes
   `marvell-docs/_build/html/`.

2. **Multi-version site** — [`_scripts/build-site.sh`](_scripts/build-site.sh):
   For every **published** release (tags mentioned in
   R1/marvell-docs/releases/releases.yaml), docs are generated and presented as
   drop-down menu in website. Each release docs separates from other release
   branch's docs.

### Workflow

- Multi-site is built for each release tag entry mentioned in
  [`releases.yaml`](https://github.com/Marvell-Lab/sonic-buildimage/blob/rls-202511.01/marvell-docs/SONIC/releases/releases.yaml).
  Docs generation fails either release-tag is not applied or entry missing in
  `releases.yaml` file.
- Release tags is in format `rls-<majorno>.<sonic-branch>.<minorno>[_rcX]` and
  can be on any rls-* branch

### Rolling commits over release-tag

Typically docs are generated corresponding to a release-tag. However on latest
release-tag(on a branch), any new doc commits becomes part of that tag's
documentation until next-tag on that branch is not applied. As soon as next-tag
is applied, newest doc-commits becomes part of `next-tag` docs. The previous
release-tag documentation goes back to commit-hash on which release-tag is
applied.

### R1 is the main docs branch

R1 is the main branch for generating the website. That is why
[`releases.yaml`](https://github.com/Marvell-Lab/sonic-buildimage/blob/rls-202511.01/marvell-docs/SONIC/releases/releases.yaml)
is relevant and releases.yaml on other release branches are NO-OP.

However other rls-* branches must have following changes
- **marvell-docs**: Each docs content per release is separate and independent.
  It is possible to have separate layout per release tags
- **docs.yml**: Each rls-* branch should have `docs.yml` file to allow to
  generate docs when any new commits is pushed to these branche
- **release-notes.md**: Each rls-* has to maintain separate [`releases
  notes`](https://github.com/Marvell-Lab/sonic-buildimage/blob/rls-20605.01/marvell-docs/SONIC/releases/releases-notes.md).
  Docs scripts adds release-tags and hyperlinks to
  [`release`](https://jubilant-adventure-gwy7y5m.pages.github.io/02.202605.01_rc0/SONIC/releases/index.html)
  page.
