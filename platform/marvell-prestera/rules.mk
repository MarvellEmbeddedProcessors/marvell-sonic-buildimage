include $(PLATFORM_PATH)/sai.mk
include $(PLATFORM_PATH)/docker-syncd-mrvl-prestera.mk
include $(PLATFORM_PATH)/docker-syncd-mrvl-prestera-rpc.mk
include $(PLATFORM_PATH)/docker-saiserver-mrvl-prestera.mk
include $(PLATFORM_PATH)/libsaithrift-dev.mk
include $(PLATFORM_PATH)/one-image.mk
include $(PLATFORM_PATH)/platform-marvell.mk
ifeq ($(CONFIGURED_ARCH),$(filter $(CONFIGURED_ARCH),arm64 armhf))
include $(PLATFORM_PATH)/mrvl-prestera.mk
include $(PLATFORM_PATH)/platform-nokia.mk
endif

SONIC_ALL += $(SONIC_ONE_IMAGE) \
             $(DOCKER_FPM) 	\
             $(DOCKER_SYNCD_MRVL_RPC)

# Inject mrvl-prestera sai into syncd. This applies to every real-hardware
# marvell-prestera build -- arm64/armhf ASICs *and* amd64 Falcon boards
# (mrvllibsai is published per-arch, including amd64; see sai.mk and the
# amd64 FALCON_* LAZY_INSTALLS in one-image.mk). Skip only when building the
# marvell-prestera-psai-vs (white-model) flavor: that flavor is also amd64,
# but uses the locally-built white-model libsai instead (wired in below), so
# guard on the flag itself rather than on CONFIGURED_ARCH.
ifneq ($(BUILD_MRVL_PRESTERA_PSAI_VS),y)
$(SYNCD)_DEPENDS += $(MRVL_SAI)
$(SYNCD)_UNINSTALLS += $(MRVL_SAI)
endif

ifeq ($(ENABLE_SYNCD_RPC),y)
$(SYNCD)_DEPENDS := $(filter-out $(LIBTHRIFT_DEV),$($(SYNCD)_DEPENDS))
$(SYNCD)_DEPENDS += $(LIBSAITHRIFT_DEV)
endif

# Runtime dependency on mrvl-prestera sai is set only for syncd
ifneq ($(BUILD_MRVL_PRESTERA_PSAI_VS),y)
$(SYNCD)_RDEPENDS += $(MRVL_SAI)
endif

# marvell-prestera-psai-vs (amd64 white-model) flavor. The Prestera CPSS white
# model (PSAI) is shipped in its own dedicated syncd container (one libsai per
# container; no runtime switching -- selection is per-image / per-platform).
ifeq ($(BUILD_MRVL_PRESTERA_PSAI_VS),y)
include $(PLATFORM_PATH)/sai-psai-vs.mk
include $(PLATFORM_PATH)/onie.mk

# Reuse the VS platform module from platform/vs. The cross-platform include
# resolves $(PLATFORM_PATH) to platform/marvell-prestera at evaluation time,
# so override _SRC_PATH to point back at the real source tree.
include $(PLATFORM_PATH)/../vs/platform-modules-vs.mk
$(VS_PLATFORM_MODULE)_SRC_PATH := $(PLATFORM_PATH)/../vs/sonic-platform-modules-vs

# $(SYNCD) (syncd_1.0.0_$(CONFIGURED_ARCH).deb) is shared with the real-hardware
# syncd docker and is built WITHOUT --with-sai=vs, so its configure step
# auto-detects a generic -lsai / <sai/sai.h>. For this flavor that must come
# from the locally-built white-model libsai deb (ships /usr/lib/libsai.so +
# /usr/include/sai headers). syncd is SAI-agnostic at runtime: the syncd
# container COPYs its own libsai.so over the top.
$(SYNCD)_DEPENDS += $(MARVELL_PRESTERA_PSAI_VS_LIBSAI)
$(SYNCD)_RDEPENDS += $(MARVELL_PRESTERA_PSAI_VS_LIBSAI)
# Uninstall our libsai from the build container once syncd is built (mirrors the
# real-hw $(SYNCD)_UNINSTALLS += $(MRVL_SAI) above, which is skipped for this
# flavor). Together with the conflict declared in sai-psai-vs.mk this lets the
# always-built libsaivs-dev install for swss without colliding on
# /usr/lib/libsai.so + /usr/include/sai headers.
$(SYNCD)_UNINSTALLS += $(MARVELL_PRESTERA_PSAI_VS_LIBSAI)
# Also uninstall the real-hardware Marvell SAI. Even though $(SYNCD) does not
# directly depend on $(MRVL_SAI) for this flavor (guarded above by
# BUILD_MRVL_PRESTERA_PSAI_VS), libsaithrift-dev DOES
# ($(LIBSAITHRIFT_DEV)_DEPENDS += $(MRVL_SAI) in libsaithrift-dev.mk,
# unconditionally for every CONFIGURED_ARCH), and ENABLE_SYNCD_RPC=y pulls
# libsaithrift-dev into $(SYNCD)_DEPENDS. That installs mrvllibsai into the
# build container early on. mrvllibsai conflicts with libsaivs-dev (sai.mk),
# so libsaivs-dev-install would otherwise block forever waiting for it to
# disappear. syncd is the last consumer of the vendor SAI, so uninstalling it
# here (exactly like the real-hw path) lets libsaivs-dev install for swss.
$(SYNCD)_UNINSTALLS += $(MRVL_SAI)

include $(PLATFORM_PATH)/docker-syncd-marvell-prestera-psai-vs.mk
include $(PLATFORM_PATH)/one-image-psai-vs.mk
include $(PLATFORM_PATH)/kvm-image-psai-vs.mk

SONIC_ALL += $(SONIC_MARVELL_PRESTERA_PSAI_VS_ONE_IMAGE) \
             $(SONIC_MARVELL_PRESTERA_PSAI_VS_KVM_IMAGE)
endif
