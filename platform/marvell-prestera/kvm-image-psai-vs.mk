# sonic marvell-prestera-psai-vs kvm image

SONIC_MARVELL_PRESTERA_PSAI_VS_KVM_IMAGE = sonic-marvell-prestera-psai-vs.img.gz
$(SONIC_MARVELL_PRESTERA_PSAI_VS_KVM_IMAGE)_INSTALLS += $(SYSTEMD_SONIC_GENERATOR)
$(SONIC_MARVELL_PRESTERA_PSAI_VS_KVM_IMAGE)_LAZY_INSTALLS += $(VS_PLATFORM_MODULE)
$(SONIC_MARVELL_PRESTERA_PSAI_VS_KVM_IMAGE)_MACHINE = marvell-prestera-psai-vs
$(SONIC_MARVELL_PRESTERA_PSAI_VS_KVM_IMAGE)_IMAGE_TYPE = kvm
# $(SONIC_INSTALL_DOCKER_IMAGES)/_DBG_IMAGES are shared across the real-hardware
# and marvell-prestera-psai-vs syncd dockers (both get registered into the same
# global list). Filter out the real-hardware syncd docker here so this VS
# image doesn't try to pull in mrvllibsai / the vendor SAI (this flavor ships
# its own white-model libsai via the dedicated psai-vs syncd docker instead).
ifeq ($(INSTALL_DEBUG_TOOLS),y)
$(SONIC_MARVELL_PRESTERA_PSAI_VS_KVM_IMAGE)_DOCKERS += $(filter-out $(DOCKER_SYNCD_BASE_DBG), $(SONIC_INSTALL_DOCKER_DBG_IMAGES))
$(SONIC_MARVELL_PRESTERA_PSAI_VS_KVM_IMAGE)_DOCKERS += $(filter-out $(DOCKER_SYNCD_BASE) $(patsubst %-$(DBG_IMAGE_MARK).gz,%.gz, $(SONIC_INSTALL_DOCKER_DBG_IMAGES)), $(SONIC_INSTALL_DOCKER_IMAGES))
else
$(SONIC_MARVELL_PRESTERA_PSAI_VS_KVM_IMAGE)_DOCKERS = $(filter-out $(DOCKER_SYNCD_BASE), $(SONIC_INSTALL_DOCKER_IMAGES))
endif
$(SONIC_MARVELL_PRESTERA_PSAI_VS_KVM_IMAGE)_FILES = $(ONIE_RECOVERY_IMAGE) $(ONIE_RECOVERY_KVM_4ASIC_IMAGE) $(ONIE_RECOVERY_KVM_6ASIC_IMAGE)
SONIC_INSTALLERS += $(SONIC_MARVELL_PRESTERA_PSAI_VS_KVM_IMAGE)
