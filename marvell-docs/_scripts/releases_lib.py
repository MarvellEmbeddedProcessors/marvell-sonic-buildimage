#!/usr/bin/env python3
"""Shared release discovery for the docs table and version switcher.

A release appears in the table and in the version drop-down only when:

  1. It exists as a git tag matching ``rls-*`` (any suffix, including ``_rcN``), and
  2. It has a matching entry in ``SONIC/releases/releases.yaml``.

Exactly one yaml entry should set ``latest: true``; that release is listed first
in the switcher as ``<version> (latest)`` and is the site-root redirect target.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

_RELEASES_DIR = Path(__file__).resolve().parents[1] / "SONIC" / "releases"
_META_FILE = _RELEASES_DIR / "releases.yaml"

_TAG_PREFIX = "rls-"


def tag_to_version(tag: str) -> str:
    """Docs deploy folder / switcher version for a tag (strip ``rls-``)."""
    if tag.startswith(_TAG_PREFIX):
        return tag[len(_TAG_PREFIX) :]
    return tag


def _git_tags() -> set[str]:
    try:
        out = subprocess.check_output(
            ["git", "tag", "-l", "rls-*"],
            cwd=str(_RELEASES_DIR),
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.SubprocessError):
        return set()
    return {line.strip() for line in out.splitlines() if line.strip()}


def load_releases() -> dict[str, dict]:
    """Per-tag metadata from ``releases.yaml`` (``releases:`` map)."""
    if not _META_FILE.is_file():
        return {}
    try:
        import yaml
    except ImportError:
        return {}
    data = yaml.safe_load(_META_FILE.read_text(encoding="utf-8")) or {}
    raw = data.get("releases", {}) or {}
    return {k: (v or {}) for k, v in raw.items() if k.startswith(_TAG_PREFIX)}


def published_tags(meta: dict | None = None) -> list[str]:
    """Git ``rls-*`` tags that also have a ``releases.yaml`` entry, newest first.

    ``DOCS_RELEASE_TAGS`` (space-separated) overrides git for local testing.
    """
    meta = meta if meta is not None else load_releases()
    env = os.environ.get("DOCS_RELEASE_TAGS")
    if env is not None:
        git_tags = {t.strip() for t in env.split() if t.strip().startswith(_TAG_PREFIX)}
    else:
        git_tags = _git_tags()
    matched = sorted(git_tags & set(meta.keys()), key=_sort_key, reverse=True)
    return matched


def latest_tag(meta: dict, tags: list[str]) -> str | None:
    """Tag marked ``latest: true``, or ``None`` if none / no tags."""
    if not tags:
        return None
    flagged = [t for t in tags if meta.get(t, {}).get("latest")]
    if len(flagged) > 1:
        raise ValueError(
            "releases.yaml: only one release may set latest: true "
            f"(found: {', '.join(flagged)})"
        )
    return flagged[0] if flagged else None


def switcher_version_match(
    build_version: str, meta: dict | None = None, tags: list[str] | None = None
) -> str:
    """Value for the theme switcher's ``version_match`` on this build."""
    meta = meta if meta is not None else load_releases()
    tags = tags if tags is not None else published_tags(meta)
    published_versions = {tag_to_version(t) for t in tags}
    if build_version in published_versions:
        return build_version
    lt = latest_tag(meta, tags)
    return tag_to_version(lt) if lt else build_version


def switcher_entries(pages_base: str, meta: dict | None = None) -> list[dict]:
    """Version-switcher list from yaml + git (not from filesystem folders)."""
    meta = meta if meta is not None else load_releases()
    tags = published_tags(meta)
    latest = latest_tag(meta, tags)
    base = pages_base.rstrip("/")

    ordered: list[str] = []
    if latest and latest in tags:
        ordered.append(latest)
    ordered.extend(t for t in tags if t != latest)

    return [
        {
            "version": tag_to_version(tag),
            "name": (
                f"{tag_to_version(tag)} (latest)"
                if tag == latest
                else tag_to_version(tag)
            ),
            "url": f"{base}/{tag_to_version(tag)}/",
        }
        for tag in ordered
    ]


def release_branch(tag: str, info: dict) -> str:
    """Release branch column; optional ``release_branch`` in yaml overrides derivation."""
    if info.get("release_branch"):
        return info["release_branch"]
    base_version = re.sub(r"_rc\d+$", "", tag_to_version(tag))
    parts = base_version.split(".")
    if len(parts) >= 3:
        return f"rls-{parts[1]}.{parts[2]}"
    if len(parts) == 2:
        return f"rls-{parts[0]}.{parts[1]}"
    return "TBD"


def _sort_key(tag: str) -> tuple:
    """Sort tags newest-first (numeric segments, then RC index)."""
    version = tag_to_version(tag)
    rc_m = re.search(r"_rc(\d+)$", version)
    rc = int(rc_m.group(1)) if rc_m else -1
    base = re.sub(r"_rc\d+$", "", version)
    nums: tuple[int, ...] = tuple()
    for part in base.split("."):
        try:
            nums += (int(part),)
        except ValueError:
            nums += (0,)
    return (nums, rc)


def _cli() -> int:
    parser = argparse.ArgumentParser(description="Release metadata helpers")
    parser.add_argument("--list-tags", action="store_true")
    parser.add_argument("--latest-version", action="store_true")
    args = parser.parse_args()
    meta = load_releases()
    tags = published_tags(meta)
    if args.list_tags:
        for t in tags:
            print(t)
    if args.latest_version:
        lt = latest_tag(meta, tags)
        if lt:
            print(tag_to_version(lt))
        return 0 if lt else 1
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
