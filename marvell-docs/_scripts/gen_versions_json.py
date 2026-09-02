#!/usr/bin/env python3
"""Generate the version-switcher ``versions.json`` from published folders.

Called by ``.github/workflows/docs.yml`` on every deploy. It scans the
``gh-pages`` work tree for per-version subfolders (e.g. ``202511.01``,
``01.202511.01``) and writes ``<site_root>/versions.json`` listing them, so the
navbar version switcher always reflects exactly what is published -- there is no
hand-maintained list to keep in sync.

The default branch's version is placed first and marked "(latest)"; the rest are
listed newest-first. Every URL is rooted at ``pages_base`` (which must match the
switcher's ``json_url`` in ``conf.py``).

Usage:
    gen_versions_json.py <site_root> <default_version> <pages_base_url>
"""
from __future__ import annotations

import json
import os
import re
import sys

_VERSION_RE = re.compile(r"\d+(?:\.\d+)+")


def _is_version_dir(name: str) -> bool:
    """True for a published version folder: "master" or dotted numeric."""
    return name == "master" or bool(_VERSION_RE.fullmatch(name))


def generate(site_root: str, default_version: str, pages_base: str) -> list[dict]:
    base = pages_base.rstrip("/")
    found = sorted(
        (
            d
            for d in os.listdir(site_root)
            if os.path.isdir(os.path.join(site_root, d))
            and not d.startswith((".", "_"))
            and _is_version_dir(d)
        ),
        reverse=True,
    )
    # Default branch's version first (marked latest), then the rest newest-first.
    ordered = ([default_version] if default_version in found else []) + [
        v for v in found if v != default_version
    ]
    entries = [
        {
            "version": v,
            "name": f"{v} (latest)" if v == default_version else v,
            "url": f"{base}/{v}/",
        }
        for v in ordered
    ]
    with open(os.path.join(site_root, "versions.json"), "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)
        f.write("\n")
    return entries


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(
            "usage: gen_versions_json.py <site_root> <default_version> <pages_base_url>"
        )
    result = generate(sys.argv[1], sys.argv[2], sys.argv[3])
    print("versions.json ->", [e["version"] for e in result])
