# {{ release_tag }}

## SONiC Base Commit

| BRANCH | Base Commit Hash |
|---|---|
| [202605](https://github.com/sonic-net/sonic-buildimage/tree/202605) | [08559af01eaca653c0345ba07785322d6f9bcfb6](https://github.com/sonic-net/sonic-buildimage/commit/08559af01eaca653c0345ba07785322d6f9bcfb6) |

## SAI Version Compatibility

| | Version |
|---|---|
| Compatible OCP SAI Version | [SAI-1.18.1](https://github.com/opencomputeproject/SAI/releases/tag/v1.18.1) |

## New Features

- **VRRP support** — VRRPv4 and VRRPv6 are now available when `frr_mgmt_framework_config` is enabled:
  - **`src/sonic-swss`:** add `vrrpsyncd`, `vrrpmgrd`, and `vrrporch`; defer the virtual router interface until the parent router interface is ready.
  - **`src/sonic-utilities`:** require `frr_mgmt_framework_config` for VRRP and VRRP6 CLI commands, fix Generic Config Updater ordering for key-based CONFIG_DB dependencies, reject duplicate static-route nexthops, and add test coverage.
  - **`sonic-buildimage`:** FRR `vrrp6` and track-interface patch, `frrcfgd` handlers for `VRRP`, `VRRP6`, and track tables, `sonic-vrrp.yang`, `vrrpd` and VRRP sync/mgr processes in the FRR and orchagent containers, and a CoPP limit of 1000 pps for combined v4 and v6.

## Known Issues

