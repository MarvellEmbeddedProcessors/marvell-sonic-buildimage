# Details

Status and highlights for each supported Prestera SONiC release branch. Each
release has its own page with detailed notes.

## Naming Convention

```{image} ../about/images/release-naming-convention.svg
:alt: Release naming convention
:align: center
```

## Prestera SONiC Releases

One row per Prestera SONiC release. The list is generated from the repo's
release tags at build time (see `_scripts/gen_releases_table.py`); each release
tag links to that release's own notes.

```{include} _releases_table.md
```

### Lifecycle

**In Development**
: Branch is not yet released and is in active development with bug fixes
  and new feature additions.

**Released Active**
: Branch is released for customers and also in active development for bug
  fixes.

**Released Inactive**
: Branch is released for customers and no active development is happening
  from Marvell. Bug fixes can be received on these branches.
