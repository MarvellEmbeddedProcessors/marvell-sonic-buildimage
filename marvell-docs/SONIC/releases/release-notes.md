# {{ release_tag }}

## SONiC Base Commit

| BRANCH | Base Commit Hash |
|---|---|
| [202511](https://github.com/sonic-net/sonic-buildimage/tree/202511) | [97a82c196d58bbb39567da9ca991480d158a8112](https://github.com/sonic-net/sonic-buildimage/commit/97a82c196d58bbb39567da9ca991480d158a8112) |

## SAI Version Compatibility

| | Version |
|---|---|
| Compatible OCP SAI Version | [SAI-1.17.1](https://github.com/opencomputeproject/SAI/releases/tag/v1.17.1) |

## New Features

- **PVST support** — PVST is now fully functional:
  - **`src/sonic-stp`:** correct VLAN for untagged PVST BPDUs, consistent IPC struct packing, and interface/socket error handling.
  - **`src/sonic-swss`:** ebtables→nft filtering for PVST, `proto_mode` in `STP_IPC_MSG`, and stpmgr fixes.
  - **`src/sonic-utilities`:** correct STP table name and mode keyword in CLI handlers, plus added test coverage.
  - **`sonic-buildimage`:** build/docker updates to bring up the STP service.

## Known Issues

*(None yet.)*
