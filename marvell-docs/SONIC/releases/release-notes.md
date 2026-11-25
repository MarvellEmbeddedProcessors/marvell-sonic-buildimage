# {{ release_tag }}

## SONiC Base Commit

| BRANCH | Base Commit Hash |
|---|---|
| [202605](https://github.com/sonic-net/sonic-buildimage/tree/202605) | [08559af01eaca653c0345ba07785322d6f9bcfb6](https://github.com/sonic-net/sonic-buildimage/commit/08559af01eaca653c0345ba07785322d6f9bcfb6) |

## SAI Version Compatibility

| | Version |
|---|---|
| Compatible OCP SAI Version | [SAI-1.18.1](https://github.com/opencomputeproject/SAI/releases/tag/v1.18.1) |
| Marvell SAI Debian package | `mrvllibsai` 1.18.1-3 (PSAI 8.20.0) or later.|

## New Features

- **EVPN (VXLAN)** — L2 EVPN over VXLAN (single-homed): BGP EVPN control plane, VLAN-to-VNI mapping, and host-to-host traffic across the tunnel:
  - **`src/sonic-swss`:** create a point-to-point VXLAN tunnel for each remote VTEP as per SAI capability; reuse an existing VTEP for the same source IP.
  - **`src/sonic-utilities`:** `show mac` (`fdbshow`) shows the remote VTEP IP for remote VXLAN MAC entries.
  - **SAI:** fixed issues in SAI for EVPN.
- **VRRP support** — VRRPv4 and VRRPv6 are now available when `frr_mgmt_framework_config` is enabled:
  - **`src/sonic-swss`:** add `vrrpsyncd`, `vrrpmgrd`, and `vrrporch`; defer the virtual router interface until the parent router interface is ready.
  - **`src/sonic-utilities`:** require `frr_mgmt_framework_config` for VRRP and VRRP6 CLI commands, fix Generic Config Updater ordering for key-based CONFIG_DB dependencies, reject duplicate static-route nexthops, and add test coverage.
  - **`sonic-buildimage`:** FRR `vrrp6` and track-interface patch, `frrcfgd` handlers for `VRRP`, `VRRP6`, and track tables, `sonic-vrrp.yang`, `vrrpd` and VRRP sync/mgr processes in the FRR and orchagent containers, and a CoPP limit of 1000 pps for combined v4 and v6.
- **MSTP/PVST support** — MSTP/PVST is fully functional (ported from the [R1 release](https://marvellembeddedprocessors.github.io/marvell-sonic-buildimage/01.202511.01/SONIC/releases/release-notes.html#new-features)):
  - **`src/sonic-stp`:** correct VLAN for untagged PVST BPDUs, consistent IPC struct packing, and interface/socket error handling.
  - **`src/sonic-swss`:** ebtables to nft filtering for PVST, `proto_mode` in `STP_IPC_MSG`, and stpmgr fixes.
  - **`src/sonic-utilities`:** correct STP table name and mode keyword in CLI handlers, plus added test coverage.
  - **`sonic-buildimage`:** build/docker updates to bring up the STP service.
- **SONiC deployment profile** — Refer to [SONiC Deployment Profile HLD](https://github.com/sonic-net/SONiC/pull/2479).
  - **`sonic-buildimage`:** fixed inconsistencies with the build-time variables `INCLUDE_XXX`, `ENABLE_XXX` and `AUTORESTART_XXX`. 
    - Added the `ENTERPRISE` and `DATACENTER` profiles.
- **ECN / WRED**:
  - **SAI:** fixed issues in SAI for ECN/WRED.

## Known Issues

- **PVST:** warmboot is allowed when PVST is enabled. In future releases, warmboot will be disabled when PVST is enabled.
- **EVPN:** point-to-multipoint (P2MP) VXLAN tunnels are not supported. EVPN works with point-to-point tunnels to each remote VTEP only.

