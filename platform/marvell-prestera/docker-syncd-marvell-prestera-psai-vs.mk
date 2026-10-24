# docker image for marvell-prestera-psai-vs syncd

DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS = docker-syncd-marvell-prestera-psai-vs.gz
DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS_DBG = docker-syncd-marvell-prestera-psai-vs-$(DBG_IMAGE_MARK).gz

$(DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS)_PATH = $(PLATFORM_PATH)/docker-syncd-marvell-prestera-psai-vs

$(DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS)_LOAD_DOCKERS += $(DOCKER_CONFIG_ENGINE_TRIXIE)
$(DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS)_DBG_DEPENDS += $($(DOCKER_CONFIG_ENGINE_TRIXIE)_DBG_DEPENDS)
$(DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS)_DBG_IMAGE_PACKAGES = $($(DOCKER_CONFIG_ENGINE_TRIXIE)_DBG_IMAGE_PACKAGES)

SONIC_DOCKER_IMAGES += $(DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS)
# The white-model (psai-vs) flavor ships a single syncd container and has no
# separate -rpc variant (unlike the real-hardware docker-syncd-mrvl-prestera /
# docker-syncd-mrvl-prestera-rpc pair). It must therefore be installed for the
# image regardless of ENABLE_SYNCD_RPC. Guarding it behind "ifneq RPC != y" (as
# the real-hw non-rpc docker does) would, with ENABLE_SYNCD_RPC=y, leave the
# marvell-prestera-psai-vs image with no syncd start script of its own: the only
# "syncd" start script would come from the real-hw -rpc docker (MACHINE=
# marvell-prestera), so build_debian.sh's per-machine copy
# ([ -f $TARGET_MACHINE_syncd.sh ] ... else cp syncd.sh) finds neither
# marvell-prestera-psai-vs_syncd.sh nor a generic syncd.sh and fails.
SONIC_INSTALL_DOCKER_IMAGES += $(DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS)

SONIC_DOCKER_DBG_IMAGES += $(DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS_DBG)
SONIC_INSTALL_DOCKER_DBG_IMAGES += $(DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS_DBG)

$(DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS)_DEPENDS += $(SYNCD)
$(DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS)_DEPENDS += $(MARVELL_PRESTERA_PSAI_VS_LIBSAI)

ifeq ($(INSTALL_DEBUG_TOOLS), y)
$(DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS)_DBG_DEPENDS += $(SYNCD_DBG) \
                                                $(LIBSWSSCOMMON_DBG) \
                                                $(LIBSAIMETADATA_DBG) \
                                                $(LIBSAIREDIS_DBG)
endif

$(DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS)_VERSION = 1.0.0
$(DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS)_PACKAGE_NAME = syncd-vs
$(DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS)_MACHINE = marvell-prestera-psai-vs
$(DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS)_CONTAINER_NAME = syncd
$(DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS)_RUN_OPT += --privileged -t
$(DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS)_RUN_OPT += -v /host/machine.conf:/etc/machine.conf
$(DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS)_RUN_OPT += -v /etc/sonic:/etc/sonic:ro
$(DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS)_RUN_OPT += -v /host/warmboot:/var/warmboot

SONIC_TRIXIE_DOCKERS += $(DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS)
SONIC_TRIXIE_DBG_DOCKERS += $(DOCKER_SYNCD_MARVELL_PRESTERA_PSAI_VS_DBG)
