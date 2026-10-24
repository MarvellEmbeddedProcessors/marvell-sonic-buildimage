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
	rm -rf $(DEST)/.mrvlvslibsai-repack
	dpkg-deb -R $(DEST)/$(notdir $@) $(DEST)/.mrvlvslibsai-repack
	sed -i 's/^Package:.*/Package: mrvlvslibsai/' $(DEST)/.mrvlvslibsai-repack/DEBIAN/control
	printf '%s\n' '#!/bin/sh' 'set -e' \
		'case "$$1" in install|upgrade)' \
		'  dpkg-divert --package mrvlvslibsai --quiet --rename --add /usr/lib/x86_64-linux-gnu/libsaivs.so.0.0.0 || true' \
		'  dpkg-divert --package mrvlvslibsai --quiet --rename --add /usr/bin/mrvlcmd || true ;;' \
		'esac' 'exit 0' > $(DEST)/.mrvlvslibsai-repack/DEBIAN/preinst
	printf '%s\n' '#!/bin/sh' 'set -e' \
		'case "$$1" in remove|purge)' \
		'  dpkg-divert --package mrvlvslibsai --quiet --rename --remove /usr/lib/x86_64-linux-gnu/libsaivs.so.0.0.0 || true' \
		'  dpkg-divert --package mrvlvslibsai --quiet --rename --remove /usr/bin/mrvlcmd || true ;;' \
		'esac' 'exit 0' > $(DEST)/.mrvlvslibsai-repack/DEBIAN/postrm
	chmod 0755 $(DEST)/.mrvlvslibsai-repack/DEBIAN/preinst $(DEST)/.mrvlvslibsai-repack/DEBIAN/postrm
	dpkg-deb -b $(DEST)/.mrvlvslibsai-repack $(DEST)/$(notdir $@)
	rm -rf $(DEST)/.mrvlvslibsai-repack

.PHONY: clean
clean:
	rm -f $(DEST)/mrvlvslibsai_*_amd64.deb
