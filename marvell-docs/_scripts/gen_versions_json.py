#!/usr/bin/env python3
"""Generate ``versions.json`` for the navbar version switcher.

The list comes from ``releases.yaml`` entries that also exist as git ``rls-*``
tags (see ``releases_lib.py``), not from scanning deploy folders. The entry
marked ``latest: true`` is first and labelled ``(latest)``.

Usage:
    gen_versions_json.py <site_root> <pages_base_url>
"""
from __future__ import annotations

import json
import sys

from releases_lib import switcher_entries


def generate(site_root: str, pages_base: str) -> list[dict]:
    entries = switcher_entries(pages_base)
    with open(f"{site_root.rstrip('/')}/versions.json", "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)
        f.write("\n")
    return entries


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: gen_versions_json.py <site_root> <pages_base_url>")
    result = generate(sys.argv[1], sys.argv[2])
    print("versions.json ->", [e["version"] for e in result])
