# Marvell Prestera white-model SAI deb for the marvell-prestera-psai-vs (amd64)
# flavor.
#
# The SAI is built FROM SOURCE and ships /usr/lib/libsai.so (+ /usr/include/sai
# headers, + a /lib/x86_64-linux-gnu/libsaivs.so.0.0.0 alias so it can back a
# SONiC-vs image). It is embedded in the dedicated PSAI syncd container.

# ---- PSAI (Prestera CPSS white model) ----
# The build wrapper platform/marvell-prestera/sai-psai-vs/Makefile runs
# `make sai` + build_sai_debian_pkg.sh inside the submodule and drops the deb
# at $(DEST). NOTE: build_sai_debian_pkg.sh derives the version from
# saiversion.h + release_versions.txt; keep the release string below in sync
# (the wrapper renames whatever it produces to this expected filename).
MARVELL_PRESTERA_PSAI_VS_SAI_RELEASE = 1.18.1-2
MARVELL_PRESTERA_PSAI_VS_LIBSAI = mrvlvslibsai_$(MARVELL_PRESTERA_PSAI_VS_SAI_RELEASE)_amd64.deb
$(MARVELL_PRESTERA_PSAI_VS_LIBSAI)_SRC_PATH = $(PLATFORM_PATH)/sai-psai-vs
SONIC_MAKE_DEBS += $(MARVELL_PRESTERA_PSAI_VS_LIBSAI)

# Like every real-hardware SAI, our white-model libsai ships /usr/lib/libsai.so
# and /usr/include/sai/*.h, which collide with the always-built libsaivs-dev.
# Declare the conflict (mirrors platform/marvell-prestera/sai.mk for MRVL_SAI)
# so the two are never dpkg-installed into the build container simultaneously;
# rules.mk pairs this with $(SYNCD)_UNINSTALLS to break the install ordering.
$(eval $(call add_conflict_package,$(MARVELL_PRESTERA_PSAI_VS_LIBSAI),$(LIBSAIVS_DEV)))
