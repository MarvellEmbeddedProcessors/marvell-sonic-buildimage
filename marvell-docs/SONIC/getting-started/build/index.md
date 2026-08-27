# Build

## Overview

Upstream SONiC documentation provides a comprehensive guide to building SONiC
from source. See the
[sonic-buildimage
README](https://github.com/sonic-net/sonic-buildimage/blob/master/README.md)
for the full upstream reference.

This page focuses on what it takes to build **Marvell Prestera SONiC** —
prerequisites, caching, platform-specific native build steps, and the meaning
of common build arguments.

## Prerequisites

Your build machine must meet the hardware and software requirements described
in the upstream SONiC documentation. In particular, ensure the host has
sufficient CPU, memory, and disk space for a full SONiC image build. Refer to
the [sonic-buildimage
README](https://github.com/sonic-net/sonic-buildimage/blob/master/README.md#hardware)
for the recommended build-machine specifications.

## Build Cache

SONiC supports caching to speed up iterative builds. Two separate cache systems
are involved:

- **DPKG cache** — stores built artifacts such as *.deb* packages and Docker
  image tarballs. On a subsequent build, unchanged components are restored from
  cache instead of being rebuilt.
- **Version cache** — stores downloaded dependencies (pip packages, wget files,
  git clones, Docker base images) used during the build. This avoids
  re-downloading pinned dependencies on every build.

See [Caching](#caching) under Build Arguments for descriptions of
*SONIC_DPKG_CACHE_METHOD*, *SONIC_DPKG_CACHE_SOURCE*, and
*SONIC_VERSION_CACHE_METHOD*.

(build-cache-path)=
### BUILD_CACHE_PATH

*BUILD_CACHE_PATH* is the path to a shared cache directory (for example, an NFS
mount) that persists built artifacts and downloaded dependencies across builds.
It is passed to the build through *SONIC_DPKG_CACHE_SOURCE*:

- In *make configure*, set *SONIC_DPKG_CACHE_SOURCE* to this path so the build
  environment is created with the cache location configured.
- In the follow-up *make* command that builds the installer image, pass the same
  *SONIC_DPKG_CACHE_SOURCE* value again so the actual build reads and writes
  cache entries from that path.

Use the same path on both commands to avoid a mismatch between the configured
build environment and the build step. See [Caching](#caching) for how this
relates to the other cache-related arguments.

## Build for Native ARM64

Native ARM builds target Prestera platforms with an external ARM CPU (for
example, OCTEON TX2 CN9131).

### Platform support

See the [supported Marvell
platforms](../marvell-prestera/index.md#prestera-sonic-support) table for
arm64 boards and SKUs.

### Build Commands

Both *make configure* and *make target* accept additional arguments beyond those
shown below. Please refer to the [SONiC build
documentation](https://github.com/sonic-net/sonic-buildimage/blob/master/README.md)
for more details.

```bash
$ git clone https://github.com/MarvellEmbeddedProcessors/marvell-sonic-buildimage.git
$ git checkout <branch>     # For eg: rls-202511.01
$ make init

$ make configure PLATFORM=marvell-prestera PLATFORM_ARCH=arm64 \
  DEFAULT_CONTAINER_REGISTRY=publicmirror.azurecr.io \
  SONIC_VERSION_CONTROL_COMPONENTS=py2,py3,web,git,docker \
  MIRROR_SNAPSHOT=y SONIC_BUILD_JOBS=4 \
  INCLUDE_ICCPD=y INCLUDE_NAT=y ENABLE_SYNCD_RPC=y ENABLE_ZTP=y \
  SONIC_DPKG_CACHE_METHOD=rwcache \
  SONIC_DPKG_CACHE_SOURCE=<BUILD_CACHE_PATH>

$ make DEFAULT_CONTAINER_REGISTRY=publicmirror.azurecr.io \
  SONIC_VERSION_CONTROL_COMPONENTS=py2,py3,web,git,docker \
  MIRROR_SNAPSHOT=y SONIC_BUILD_JOBS=4 \
  INCLUDE_ICCPD=y INCLUDE_NAT=y ENABLE_ZTP=y ENABLE_SYNCD_RPC=y \
  SONIC_VERSION_CACHE_METHOD=rwcache \
  target/sonic-marvell-prestera-arm64.bin \
  SONIC_DPKG_CACHE_METHOD=rwcache \
  SONIC_DPKG_CACHE_SOURCE=<BUILD_CACHE_PATH>
```

Refer to [Build Arguments](#build-arguments) for more details.

## Build for AMD64

Falcon platforms use an external x86 CPU (Intel). Build natively on an amd64
host for these platforms.

### Platform support

See the [supported Marvell
platforms](../marvell-prestera/index.md#prestera-sonic-support) table for
amd64 boards and SKUs.

### Build Commands

Both *make configure* and *make target* accept additional arguments beyond those
shown below. Please refer to the [SONiC build
documentation](https://github.com/sonic-net/sonic-buildimage/blob/master/README.md)
for more details.

```bash
$ git clone https://github.com/MarvellEmbeddedProcessors/marvell-sonic-buildimage.git
$ git checkout <branch>     # For eg: rls-202511.01
$ make init

$ make configure PLATFORM=marvell-prestera PLATFORM_ARCH=amd64 \
  DEFAULT_CONTAINER_REGISTRY=publicmirror.azurecr.io \
  SONIC_VERSION_CONTROL_COMPONENTS=py2,py3,web,git,docker \
  MIRROR_SNAPSHOT=y SONIC_BUILD_JOBS=4 \
  INCLUDE_ICCPD=y INCLUDE_NAT=y ENABLE_SYNCD_RPC=y ENABLE_ZTP=y \
  SONIC_DPKG_CACHE_METHOD=rwcache \
  SONIC_DPKG_CACHE_SOURCE=<BUILD_CACHE_PATH>

$ make DEFAULT_CONTAINER_REGISTRY=publicmirror.azurecr.io \
  SONIC_VERSION_CONTROL_COMPONENTS=py2,py3,web,git,docker \
  MIRROR_SNAPSHOT=y SONIC_BUILD_JOBS=4 \
  INCLUDE_ICCPD=y INCLUDE_NAT=y ENABLE_ZTP=y ENABLE_SYNCD_RPC=y \
  SONIC_VERSION_CACHE_METHOD=rwcache \
  target/sonic-marvell-prestera.bin \
  SONIC_DPKG_CACHE_METHOD=rwcache \
  SONIC_DPKG_CACHE_SOURCE=<BUILD_CACHE_PATH>
```

Refer to [Build Arguments](#build-arguments) for more details.

(build-arguments)=
## Build Arguments

Most flags must be passed on **both** *make configure* and *make* (or saved in
*rules/config.user*), because *configure* and the actual build each read them
independently.

**make configure** — sets up the build environment (platform rules,
*sonic-slave*, generated configs).

**make target/sonic-marvell-prestera-<arch>.bin** — builds the final ONIE
installer for Marvell Prestera on the selected architecture.

### Platform and target

**PLATFORM=marvell-prestera** — Selects *platform/marvell-prestera/* build
rules (syncd, SAI, platform packages, installer). Written to *.platform* during
configure. Required on the first *make configure*; later builds read it from
*.platform*.

**PLATFORM_ARCH=arm64** or **PLATFORM_ARCH=amd64** — Target CPU
architecture. Becomes *CONFIGURED_ARCH* and drives deb package names, Docker
layers, kernel selection, and installer naming.

**target/sonic-marvell-prestera-arm64.bin** / **target/sonic-marvell-prestera-amd64.bin**
— Final ONIE installer image for the corresponding Prestera platform and
architecture. Passed only to the *make* step, not to *configure*.

### Debian / build environment selection

The NO* flags control which Debian-based build environments are enabled. *0*
means enabled; *1* means disabled.

**NOBOOKWORM=1** — Skips the Debian 12 (bookworm) build pass.

**NOTRIXIE=0** — Enables Debian 13 (trixie) as the active build environment
(*BLDENV=trixie*, *sonic-slave-trixie*).

With **NOBOOKWORM=1** and **NOTRIXIE=0**, the build runs only on trixie.

### Mirror and reproducibility

**MIRROR_SNAPSHOT=y** — Pins Debian apt mirrors to a fixed snapshot timestamp,
giving reproducible apt package versions across builds.

**SONIC_VERSION_CONTROL_COMPONENTS=py2,py3,web,git,docker** — Enables version
pinning for Python 2/3 pip packages, wget/curl downloads, git clones, and Docker
base images. Debian package versions are controlled separately via
*MIRROR_SNAPSHOT* (the *deb* component is not included here).

**DEFAULT_CONTAINER_REGISTRY=publicmirror.azurecr.io** — Uses the Microsoft
public mirror instead of Docker Hub for base images (for example,
*publicmirror.azurecr.io/debian:trixie*).

(caching)=
### Caching

**SONIC_DPKG_CACHE_METHOD=rwcache** — Read/write cache for build artifacts
(*.deb* files, Docker *.gz* images, and similar). Restores from cache when inputs
are unchanged and saves newly built artifacts.

**SONIC_DPKG_CACHE_SOURCE=<BUILD_CACHE_PATH>** — Path to the DPKG cache
directory, mounted inside the build container (default:
*/var/cache/sonic/artifacts*). Set this to the same *BUILD_CACHE_PATH* used in
*make configure* and the follow-up *make* command. See [BUILD_CACHE_PATH](#build-cache-path).

**SONIC_VERSION_CACHE_METHOD=rwcache** — Read/write cache for downloaded
dependencies (pip, wget, git, Docker base pulls) during slave and Docker builds.
Stored under **<BUILD_CACHE_PATH>/vcache**. Passed on the *make* step.

DPKG cache avoids rebuilding unchanged components; version cache avoids
re-downloading pinned dependencies.

### Parallelism

**SONIC_BUILD_JOBS=4** — Number of parallel make jobs inside *sonic-slave*
(equivalent to *make -j 4*). Controls how many packages build concurrently.

### Enable optional SONiC protocols/functionality

**INCLUDE_ICCPD=y** — Builds *docker-iccpd* and *iccpd* for MC-LAG
(inter-chassis link aggregation). Disabled by default.

**INCLUDE_NAT=y** — Builds *docker-nat* for NAT support in SONiC. Enabled by
default; passing *y* is explicit but harmless.

**ENABLE_SYNCD_RPC=y** — Builds the RPC-enabled syncd Docker variant and
*syncd-rpc* package for SAI/thrift testing. Disabled by default.

**ENABLE_ZTP=y** — Includes Zero Touch Provisioning packages and scripts in
the installer image. Disabled by default.
