.ONESHELL:
SHELL = /bin/bash
.SHELLFLAGS += -e

MAIN_TARGET = sonic-device-data_$(SONIC_DEVICE_DATA_VERSION_FULL)_all.deb

$(addprefix $(DEST)/, $(MAIN_TARGET)): $(DEST)/% :
	pushd ./src

	# Remove any stale data
	rm -rf ./device

	# set asic type for virtual switch
	if [ "$(CONFIGURED_PLATFORM)" = "vpp" ]; then \
		echo "vpp" > ../../../device/virtual/x86_64-kvm_x86_64-r0/platform_asic; \
	elif [ "$(BUILD_MRVL_PRESTERA_PSAI_VS)" = "y" ]; then \
		printf "vs\nmarvell-prestera-psai-vs\n" > ../../../device/virtual/x86_64-kvm_x86_64-r0/platform_asic; \
	else \
		echo "vs" > ../../../device/virtual/x86_64-kvm_x86_64-r0/platform_asic; \
	fi;

	# select default HWSKU: use the requested Marvell Prestera VS HWSKU
	# (paired with the white-model SAI, see PSAI_VS_HWSKU in rules/config)
	# when building the marvell-prestera-psai-vs flavor, otherwise keep the
	# standard Force10-S6000 default used by vs/alpinevs/vpp. This
	# build-time selection is why the committed default_sku stays
	# Force10-S6000: only a -vs build repoints it, so the plain vs image
	# is unaffected.
	if [ "$(BUILD_MRVL_PRESTERA_PSAI_VS)" = "y" ]; then \
		echo "$(PSAI_VS_HWSKU) t1" > ../../../device/virtual/x86_64-kvm_x86_64-r0/default_sku; \
	else \
		echo "Force10-S6000 t1" > ../../../device/virtual/x86_64-kvm_x86_64-r0/default_sku; \
	fi;

	# Create a new dir and copy all ONIE-platform-string-named dirs into it
	mkdir ./device
	cp -r -L ../../../device/*/* ./device/

	if [ "$(CONFIGURED_PLATFORM)" = "mellanox" ]; then \
		for sai_profile in `find device/ -name sai.profile | grep simx`; do \
			echo SAI_KEY_IS_SIMX=1 >> $$sai_profile; \
		done; \
	fi;

	# Generate VS HwSKU data (lanemap.ini, coreportindexmap.ini, profiles)
	# Uses Python for ~200x faster processing than the equivalent bash loop
	#
	# Skip the generic BCM56850-flavored VS overwrites and the per-vendor HWSKU
	# auto-cloning when building for marvell-prestera. The marvell-prestera-psai-vs
	# RFS uses the Marvell Prestera VS SAI library (mrvlvslibsai) which expects
	# SAI_INIT_CONFIG_FILE=... (shipped by the HWSKU under device/marvell/), not
	# SAI_VS_SWITCH_TYPE_BCM56850. Overwriting sai.profile here would break
	# syncd-marvell-prestera-psai-vs at init.
ifneq ($(CONFIGURED_PLATFORM),marvell-prestera)
	python3 ./generate_vs_hwsku.py ../../../device
endif

	# Build the package
ifeq ($(CROSS_BUILD_ENVIRON), y)
	dpkg-buildpackage -rfakeroot -b -us -uc -a$(CONFIGURED_ARCH) -Pcross,nocheck -j$(SONIC_CONFIG_MAKE_JOBS) --admindir $(SONIC_DPKG_ADMINDIR)
else
	dpkg-buildpackage -rfakeroot -b -us -uc -j$(SONIC_CONFIG_MAKE_JOBS) --admindir $(SONIC_DPKG_ADMINDIR)
endif

	popd

	mv $* $(DEST)/
