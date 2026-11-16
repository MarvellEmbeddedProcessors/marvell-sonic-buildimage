# Marvell Prestera Platforms

## Prestera SOC Naming

```{image} ../images/prestera-soc-naming.svg
:alt: Prestera SoC naming convention
:align: center
```

## Architecture support

- **arm64**: External CPU: _OCTEON TX2 CN9131_
- **amd64** External CPU: _Intel_

(prestera-sonic-support)=
## Prestera SONiC Support

Among various platforms of Marvell Prestera, following platforms are verified
with `Prestera SONiC` releases

Platform Family | Board / SKU | Architecture | ONIE Platform String |
|---|---|---|---|
| Marvell AC5X + CN9131 | RD98DX35xx-CN9131 | arm64 | `arm64-marvell_rd98DX35xx_cn9131-r0` |
| Marvell AC5P + CN9131 | RD98DX45xx-CN9131 | arm64 | `arm64-marvell_rd98DX45xx_cn9131-r0` |
| Marvell Falcon | DB98CX8580-XX-Intel | amd64 | `x86_64-marvell_db98cx8580_32cd-r0` |
| Marvell Falcon | DB98CX8540-XX-Intel | amd64 | `x86_64-marvell_db98cx8540_16cd-r0` |
| Marvell Falcon | DB98CX8514-10CC | amd64 | `x86_64-marvell_db98cx8514_10cc-r0` |
| Marvell Falcon | DB98CX8522-10CC | amd64 | `x86_64-marvell_db98cx8522_10cc-r0` |
