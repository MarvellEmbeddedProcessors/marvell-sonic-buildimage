# Prestera SONiC Repositories

Prestera SONiC uses a **hybrid scheme** that combines open-source SONiC
repositories with Marvell-specific repositories.

Upstream SONiC repositories are used as-is so Prestera SONiC tracks the
community codebase directly. Marvell-specific repositories are used to develop
features that are not yet merged into upstream SONiC. Marvell plans to
upstream all Prestera SONiC features to upstream SONiC over time. For that
reason, features developed in Prestera SONiC follow upstream SONiC guidelines.
See [How to Contribute](../collaborate/how-to-contribute.md) for the pull request
process and Marvell-specific repository guidance.

*sonic-buildimage* is the top-level build repository that assembles SONiC using
[Git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) for every
major component (SWSS, SAI/syncd, platform drivers, management tooling, and
more). In practice, this hybrid model means most submodules are consumed
directly from upstream *sonic-net* repositories, while a smaller set of
submodules are Marvell-maintained forks that carry Prestera-specific changes.

(prestera-sonic-repos)=
## Prestera SONiC Repos

- [marvell-sonic-buildimage](https://github.com/MarvellEmbeddedProcessors/marvell-sonic-buildimage)
- [marvell-sonic-utilities](https://github.com/MarvellEmbeddedProcessors/marvell-sonic-utilities)
- [marvell-sonic-swss](https://github.com/MarvellEmbeddedProcessors/marvell-sonic-swss)
- [marvell-sonic-stp](https://github.com/MarvellEmbeddedProcessors/marvell-sonic-stp)

## Where to Look

- The full, up-to-date list of submodules and the branch/URL each one is
  pinned to is defined in the *.gitmodules* file at the root of
  *sonic-buildimage*.
- Submodule-specific changes made for a given Prestera SONiC release are
  called out in that release's page under [Details](../releases/details.md).
