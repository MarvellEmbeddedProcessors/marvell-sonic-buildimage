# {{ release_tag }}

## SONiC Base Commit

| BRANCH | Base Commit Hash |
|---|---|

## SAI Version Compatibility

| | Version |
|---|---|

## Supported Features

- **PVST support**:
  - **`src/sonic-stp`:** correct VLAN for untagged PVST BPDUs, consistent IPC struct packing, and interface/socket error handling.
  - **`src/sonic-swss`:** ebtables→nft filtering for PVST, `proto_mode` in `STP_IPC_MSG`, and stpmgr fixes.
  - **`src/sonic-utilities`:** correct STP table name and mode keyword in CLI handlers, plus added test coverage.
  - **`sonic-buildimage`:** build/docker updates to bring up the STP service.

## Known Issues

*(None yet.)*
