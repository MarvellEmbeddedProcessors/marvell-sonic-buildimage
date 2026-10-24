# Build wrapper: produce the Prestera white-model SAI deb (mrvlvslibsai) from the
# prestera-psai submodule for the marvell-prestera-psai-vs flavor.
#
# Invoked by slave.mk's SONIC_MAKE_DEBS rule as:
#   make -C platform/marvell-prestera/sai-psai-vs DEST=<abs debs dir> <abs debs dir>/<deb>
#
# The two-stage native build is:
#   1. make -C build sai              -> dist/native/libsai.so
#   2. build/build_sai_debian_pkg.sh  -> dist/mrvlvslibsai_<ver>_amd64.deb

DEST ?= $(CURDIR)
PSAI := $(CURDIR)/../prestera-psai

$(DEST)/%.deb:
	@if [ ! -x "$(PSAI)/build/build_sai_debian_pkg.sh" ]; then \
		echo "ERROR: prestera-psai submodule is not populated."; \
		echo "       Run 'make psai-sync' at the repo root first."; \
		exit 1; \
	fi
	mkdir -p $(PSAI)/dist/native
	touch $(PSAI)/dist/native/cpss_fw_done
	cd $(PSAI)/build && MAKEFLAGS= $(MAKE) cpss_apply_patch sai_apply_patch
	cd $(PSAI)/build && \
		PYINC=$$(python3-config --includes | sed 's/-I//; s/ .*//') && \
		PYVER=$$(basename $$PYINC | sed 's/python//') && \
		MAKEFLAGS= $(MAKE) -j1 PYTHONINC=$$PYINC PYTHONFLAG=-lpython$$PYVER sai
	cd $(PSAI)/build && ./build_sai_debian_pkg.sh $(patsubst mrvlvslibsai_%_amd64.deb,%,$(notdir $@)) amd64
	cp $(PSAI)/dist/mrvlvslibsai_[0-9]*_amd64.deb $(DEST)/$(notdir $@)
	# build_sai_debian_pkg.sh always hardcodes "Package: mrvllibsai" in
	# DEBIAN/control regardless of the output filename it's asked for, so the
	# deb we just copied (correctly named mrvlvslibsai_*.deb on disk) actually
	# registers itself in dpkg's database as "mrvllibsai" -- the SAME package
	# name as the real-hardware SAI from sai.mk. That defeats our
	# add_conflict_package(MARVELL_PRESTERA_PSAI_VS_LIBSAI, LIBSAIVS_DEV) wait
	# in slave.mk (which matches on this Package: field, not the filename) and
	# makes dpkg itself flag a bogus file-collision with libsaivs-dev instead
	# of the intended one. Rewrite the field in-place so the installed
	# package's identity matches its filename.
	rm -rf $(DEST)/.mrvlvslibsai-repack
	dpkg-deb -R $(DEST)/$(notdir $@) $(DEST)/.mrvlvslibsai-repack
	sed -i 's/^Package:.*/Package: mrvlvslibsai/' $(DEST)/.mrvlvslibsai-repack/DEBIAN/control
	dpkg-deb -b $(DEST)/.mrvlvslibsai-repack $(DEST)/$(notdir $@)
	rm -rf $(DEST)/.mrvlvslibsai-repack

.PHONY: clean
clean:
	rm -f $(DEST)/mrvlvslibsai_*_amd64.deb
