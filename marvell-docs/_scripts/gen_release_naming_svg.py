#!/usr/bin/env python3
"""Generate ``SONIC/about/images/release-naming-convention.svg``.

The release-naming diagram is a *generated* image that always illustrates the
canonical release *tag* form ``rls-<major>.<sonic>.<minor>`` (with the "Marvell
Release Major No." callout). It is (re)built at docs-build time via a Sphinx
``setup()`` hook in ``conf.py`` without a committed, hand-maintained image:

* tag    ``rls-<major>.<sonic>.<minor>``  e.g. ``rls-01.202511.01`` (3 parts)
  -- uses the tag's own numbers.
* branch ``rls-<sonic>.<minor>``          e.g. ``rls-202511.01``    (2 parts),
  and non-release builds -- fall back to the representative sample tag so the
  full convention (including the major) is still shown (see ``render``).

The generated SVG is git-ignored (regenerated on every build). To produce it
manually (e.g. to eyeball a change):

    python marvell-docs/_scripts/gen_release_naming_svg.py            # from $GITHUB_REF_NAME
    RELEASE_VERSION=01.202511.01 python marvell-docs/_scripts/gen_release_naming_svg.py

Requires matplotlib (in ``marvell-docs/requirements.txt``).
"""
from __future__ import annotations

import os
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "SONIC/about/images/release-naming-convention.svg"

# Sample release used to illustrate the convention when the build isn't on a
# release ref (e.g. main/master builds, where version == "master"). Uses the
# canonical release (tag) form: rls-<major>.<sonic>.<minor>.
_SAMPLE = ["01", "202511", "01"]

_LABEL_PREFIX = "Release Prefix"
_LABEL_MAJOR = "Marvell Release Major No."
_LABEL_SONIC = "Corresponding SONiC Version"
_LABEL_MINOR = "Marvell Release Minor No."

# --- Layout constants (points), tuned to match the original figure -----------
_WIDTH = 545.8275
_TITLE_BASELINE = 38.317727
_TITLE_START_X = 6.696
_TITLE_SIZE = 22
_EXAMPLE_POS = (31.929844, 14.635944)
_EXAMPLE_SIZE = 13
_LABEL_X = 336.024
_LABEL_SIZE = 12
_FIRST_ROW_Y = 57.06494
_ROW_GAP = 19.404
_LEADER_TOP_Y = 45.021443
_LEADER_GAP = 3.117657  # drop the leader to just above its caption baseline
_LINE_WIDTH = 1.8
# Each leader is an elbow arrow: a vertical drop under the segment, then a
# horizontal shaft ending in a filled arrowhead just left of the caption column.
_ARROW_TIP_X = 327.315539
_ARROWHEAD_LEN = 7.2
_ARROWHEAD_HALF = 3.6


def _release_parts(version: str) -> list[str]:
    """Numeric parts of a release version, or a representative sample."""
    parts = version.split(".")
    if len(parts) in (2, 3) and all(p.isdigit() for p in parts):
        return parts
    return _SAMPLE


def _segments(parts: list[str]) -> list[tuple[str, str | None]]:
    """Format-line segments (placeholder text, callout label)."""
    minor = parts[-1]
    major, sonic = (parts[0], parts[1]) if len(parts) == 3 else (None, parts[0])

    segs: list[tuple[str, str | None]] = [("rls", _LABEL_PREFIX), ("-", None)]
    if major is not None:
        segs += [("X" * len(major), _LABEL_MAJOR), (".", None)]
    segs += [
        ("X" * len(sonic), _LABEL_SONIC),
        (".", None),
        ("X" * len(minor), _LABEL_MINOR),
    ]
    return segs


def _draw(segments, example: str, out_path: Path) -> None:
    import matplotlib

    # Agg (not the SVG backend) so text extents can be measured via
    # get_renderer(); savefig(format="svg") still emits SVG.
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon

    plt.rcParams.update(
        {
            "svg.fonttype": "path",  # embed glyph outlines, no font dependency
            "font.family": "DejaVu Sans",
            "font.weight": "bold",
        }
    )

    n_labels = sum(1 for _, label in segments if label)
    height = _FIRST_ROW_Y + (n_labels - 1) * _ROW_GAP + 9.47

    fig = plt.figure(figsize=(_WIDTH / 72, height / 72), dpi=72)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, _WIDTH)
    ax.set_ylim(height, 0)  # y increases downward, matching SVG
    ax.axis("off")

    renderer = fig.canvas.get_renderer()
    inv = ax.transData.inverted()

    # Format line: draw each segment left-to-right, measuring widths so a leader
    # can be centred under each labelled segment.
    x = _TITLE_START_X
    labelled: list[tuple[float, str]] = []
    for text, label in segments:
        t = ax.text(x, _TITLE_BASELINE, text, size=_TITLE_SIZE, weight="bold",
                    va="baseline", ha="left")
        bb = t.get_window_extent(renderer=renderer)
        (x0, _), (x1, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
        width = x1 - x0
        if label:
            labelled.append((x + width / 2.0, label))
        x += width

    # Example line (italic), above the format line.
    ax.text(*_EXAMPLE_POS, f"Example:  {example}", size=_EXAMPLE_SIZE,
            weight="bold", style="italic", va="baseline", ha="left")

    # Captions stacked top-to-bottom, right-most segment on top (fanned leaders).
    for row, (center_x, label) in enumerate(sorted(labelled, reverse=True)):
        row_y = _FIRST_ROW_Y + row * _ROW_GAP
        arrow_y = row_y - _LEADER_GAP

        # Elbow leader: vertical drop under the segment, then a horizontal shaft
        # ending in a filled arrowhead pointing right at the caption.
        ax.plot([center_x, center_x], [_LEADER_TOP_Y, arrow_y],
                color="black", linewidth=_LINE_WIDTH, solid_capstyle="butt")
        ax.plot([center_x, _ARROW_TIP_X], [arrow_y, arrow_y],
                color="black", linewidth=_LINE_WIDTH, solid_capstyle="round")
        ax.add_patch(Polygon(
            [(_ARROW_TIP_X - _ARROWHEAD_LEN, arrow_y - _ARROWHEAD_HALF),
             (_ARROW_TIP_X, arrow_y),
             (_ARROW_TIP_X - _ARROWHEAD_LEN, arrow_y + _ARROWHEAD_HALF)],
            closed=True, facecolor="black", edgecolor="black",
            linewidth=_LINE_WIDTH, joinstyle="round"))

        ax.text(_LABEL_X, row_y, label, size=_LABEL_SIZE, weight="bold",
                va="baseline", ha="left")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, format="svg", transparent=False)
    plt.close(fig)


def render(version: str, out_path: Path | str = OUT) -> Path:
    """Render the naming-convention SVG for ``version`` to ``out_path``.

    The diagram always illustrates the canonical release *tag* form
    ``rls-<major>.<sonic>.<minor>`` (including the "Marvell Release Major No."
    callout). A release *tag* build (3-part version) uses its own numbers; a
    branch build (2-part, e.g. ``rls-202511.01``) or non-release build would
    otherwise drop the major, so those fall back to the representative sample
    tag -- the full convention is shown regardless of which ref is built.
    """
    out_path = Path(out_path)
    parts = _release_parts(version)
    if len(parts) != 3:
        parts = _SAMPLE
    _draw(_segments(parts), "rls-" + ".".join(parts), out_path)
    return out_path


def _version_from_env() -> str:
    version = os.environ.get("RELEASE_VERSION")
    if version:
        return version
    branch = os.environ.get("GITHUB_REF_NAME", "")
    return branch[len("rls-"):] if branch.startswith("rls-") else "master"


if __name__ == "__main__":
    dest = render(_version_from_env())
    print(f"Wrote {dest}")
