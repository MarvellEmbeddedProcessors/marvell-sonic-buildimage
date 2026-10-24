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

	# Skip the generic BCM56850-flavored VS overwrites and the per-vendor HWSKU
	# auto-cloning when building for marvell-prestera. The marvell-prestera-psai-vs
	# RFS uses the Marvell Prestera VS SAI library (mrvlvslibsai) which expects
	# SAI_INIT_CONFIG_FILE=... (shipped by the HWSKU under device/marvell/), not
	# SAI_VS_SWITCH_TYPE_BCM56850. Overwriting sai.profile here would break
	# syncd-marvell-prestera-psai-vs at init.
ifneq ($(CONFIGURED_PLATFORM),marvell-prestera)
	# Create hwsku for virtual switch
	for d in `find -L ../../../device -maxdepth 3 -mindepth 3 -type d | grep -vE "(plugins|led-code|sonic_platform)"`; do \
		# check if hwsku dir exists, if yes, then continue
		if [ -d device/x86_64-kvm_x86_64-r0/$$(basename $$d) ]; then \
			cp ./sai.vs_profile device/x86_64-kvm_x86_64-r0/$$(basename $$d)/sai.profile; \
			cp ./sai_mlnx.vs_profile device/x86_64-kvm_x86_64-r0/$$(basename $$d)/sai_mlnx.profile; \
			cp ./sai_vpp.vs_profile device/x86_64-kvm_x86_64-r0/$$(basename $$d)/sai_vpp.profile; \
			cp ./pai.vs_profile device/x86_64-kvm_x86_64-r0/$$(basename $$d)/pai.profile; \
			cp ./fabriclanemap_vs.ini device/x86_64-kvm_x86_64-r0/$$(basename $$d)/fabriclanemap.ini; \
			continue; \
		fi; \
		cp -Lr $$d device/x86_64-kvm_x86_64-r0/ ; \
		if [ -f $$(dirname $$d)/asic.conf ]; then \
			cp $$(dirname $$d)/asic.conf device/x86_64-kvm_x86_64-r0/$$(basename $$d)/asic.conf; \
		fi; \
		cp ./sai.vs_profile device/x86_64-kvm_x86_64-r0/$$(basename $$d)/sai.profile; \
		cp ./sai_mlnx.vs_profile device/x86_64-kvm_x86_64-r0/$$(basename $$d)/sai_mlnx.profile; \
		cp ./sai_vpp.vs_profile device/x86_64-kvm_x86_64-r0/$$(basename $$d)/sai_vpp.profile; \
		cp ./pai.vs_profile device/x86_64-kvm_x86_64-r0/$$(basename $$d)/pai.profile; \
		cp ./fabriclanemap_vs.ini device/x86_64-kvm_x86_64-r0/$$(basename $$d)/fabriclanemap.ini; \
		if [ -f device/x86_64-kvm_x86_64-r0/$$(basename $$d)/port_config.ini ]; then \
			last_line=$$(tail -n 1 device/x86_64-kvm_x86_64-r0/$$(basename $$d)/port_config.ini); \
			num_columns=$$(echo $$last_line | awk '{print NF}'); \
			i=0; \
			if [ -f $$(dirname $$d)/chassisdb.conf ] && ! grep -q '^disaggregated_chassis=1' $$(dirname $$d)/platform_env.conf; then \
				echo "Reserve midplane interface for $$(dirname $$d)"; \
				i=$$(($$i+1)); \
			fi; \
			while IFS= read -r line || [ -n "$$line" ]; do \
				if ! grep -q "^#" <<< "$$line"; then \
					i=$$(($$i+1)); \
					lanes=$$(echo "$$line" | awk '{print $$2}'); \
					echo "eth$$i:$$lanes" >> device/x86_64-kvm_x86_64-r0/$$(basename $$d)/lanemap.ini; \
					if [ $$num_columns -ge 9 ]; then \
						core=$$(echo "$$line" | awk '{print $$8}'); \
						core_port=$$(echo "$$line" | awk '{print $$9}'); \
						echo "eth$$i:$$core,$$core_port" >> device/x86_64-kvm_x86_64-r0/$$(basename $$d)/coreportindexmap.ini; \
					fi; \
				fi; \
			done < device/x86_64-kvm_x86_64-r0/$$(basename $$d)/port_config.ini; \
		fi; \
		if [ -f device/x86_64-kvm_x86_64-r0/$$(basename $$d)/context_config.json ]; then \
			rm device/x86_64-kvm_x86_64-r0/$$(basename $$d)/context_config.json; \
		fi; \
		if [ -f $$(dirname $$d)/chassisdb.conf ]; then \
			# Append Cpu0 Port in lanemap.ini
			if [ -f device/x86_64-kvm_x86_64-r0/$$(basename $$d)/lanemap.ini ]; then \
				echo "Cpu0:999" >> device/x86_64-kvm_x86_64-r0/$$(basename $$d)/lanemap.ini; \
			fi; \
			if [ -f device/x86_64-kvm_x86_64-r0/$$(basename $$d)/coreportindexmap.ini ]; then \
				echo "Cpu0:0,0" >> device/x86_64-kvm_x86_64-r0/$$(basename $$d)/coreportindexmap.ini; \
			fi; \
		fi; \
		i=0; \
		if [ -f $$(dirname $$d)/chassisdb.conf ] && ! grep -q '^disaggregated_chassis=1' $$(dirname $$d)/platform_env.conf; then \
			echo "Reserve midplane interface for $$(dirname $$d)"; \
			i=$$(($$i+1)); \
		fi; \
		subdirs="0 1 2"; \
		for subdir_idx in $$subdirs; do \
			subdir="device/x86_64-kvm_x86_64-r0/$$(basename $$d)/$$subdir_idx"; \
			if [ -d "$$subdir" ]; then \
				cp ./sai.vs_profile device/x86_64-kvm_x86_64-r0/$$(basename $$d)/$$(basename $$subdir)/sai.profile; \
				cp ./fabriclanemap_vs.ini device/x86_64-kvm_x86_64-r0/$$(basename $$d)/$$(basename $$subdir)/fabriclanemap.ini; \
				if [ -f device/x86_64-kvm_x86_64-r0/$$(basename $$d)/$$(basename $$subdir)/context_config.json ]; then \
					rm device/x86_64-kvm_x86_64-r0/$$(basename $$d)/$$(basename $$subdir)/context_config.json; \
				fi; \
				if [ -f device/x86_64-kvm_x86_64-r0/$$(basename $$d)/$$(basename $$subdir)/port_config.ini ]; then \
					last_line=$$(tail -n 1 device/x86_64-kvm_x86_64-r0/$$(basename $$d)/$$(basename $$subdir)/port_config.ini); \
					num_columns=$$(echo $$last_line | awk '{print NF}'); \
					while IFS= read -r line || [ -n "$$line" ]; do \
						if ! grep -q "^#" <<< "$$line"; then \
							i=$$(($$i+1)); \
							lanes=$$(echo "$$line" | awk '{print $$2}'); \
							echo "eth$$i:$$lanes" >> device/x86_64-kvm_x86_64-r0/$$(basename $$d)/$$(basename $$subdir)/lanemap.ini; \
							if [ $$num_columns -ge 9 ]; then \
								core=$$(echo "$$line" | awk '{print $$8}'); \
								core_port=$$(echo "$$line" | awk '{print $$9}'); \
								echo "eth$$i:$$core,$$core_port" >> device/x86_64-kvm_x86_64-r0/$$(basename $$d)/$$(basename $$subdir)/coreportindexmap.ini; \
							fi; \
						fi; \
					done < device/x86_64-kvm_x86_64-r0/$$(basename $$d)/$$(basename $$subdir)/port_config.ini; \
				fi; \
				if [ -f $$(dirname $$d)/chassisdb.conf ]; then \
					if [ -f device/x86_64-kvm_x86_64-r0/$$(basename $$d)/$$(basename $$subdir)/lanemap.ini ]; then \
						echo "Cpu0:999" >> device/x86_64-kvm_x86_64-r0/$$(basename $$d)/$$(basename $$subdir)/lanemap.ini; \
						i=$$(($$i+1)); \
					fi; \
					if [ -f device/x86_64-kvm_x86_64-r0/$$(basename $$d)/$$(basename $$subdir)/coreportindexmap.ini ]; then \
						echo "Cpu0:0,0" >> device/x86_64-kvm_x86_64-r0/$$(basename $$d)/$$(basename $$subdir)/coreportindexmap.ini; \
					fi; \
				fi; \
			fi; \
		done; \
	done;
endif

	# Build the package
ifeq ($(CROSS_BUILD_ENVIRON), y)
	dpkg-buildpackage -rfakeroot -b -us -uc -a$(CONFIGURED_ARCH) -Pcross,nocheck -j$(SONIC_CONFIG_MAKE_JOBS) --admindir $(SONIC_DPKG_ADMINDIR)
else
	dpkg-buildpackage -rfakeroot -b -us -uc -j$(SONIC_CONFIG_MAKE_JOBS) --admindir $(SONIC_DPKG_ADMINDIR)
endif

	popd

	mv $* $(DEST)/
