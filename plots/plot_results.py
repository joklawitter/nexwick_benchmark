"""Extracts hyperfine benchmark results from results/*.md and plot them.

Reading and plotting are kept in separate functions so different plot styles
can be tried on the same tidy DataFrame:

    df = read_all_results(RESULTS_DIR)   # tidy long-form table
    plot_relative_grouped(df, ...)
    plot_relative_fast(df, ...)

Run directly to regenerate every plot into plots/:

    python plot_results.py

Written by Claude Code, Opus 4.8
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- configuration ----------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = SCRIPT_DIR.parent / "results"
PLOTS_DIR = SCRIPT_DIR

# Convert every reported time to milliseconds so datasets are comparable.
UNIT_TO_MS = {"ms": 1.0, "s": 1000.0, "us": 0.001}

# results_<stem>.md  ->  display name for the dataset.
DATASET_NAMES = {
    "RSV2": "RSV2",
    "aars": "aars",
    "cephalopods": "cephalopods",
    "dplace": "D-PLACE",
}

# Order parsers roughly fastest -> slowest for consistent, readable axes.
PARSER_ORDER = [
    "nexwick (lazy)",
    "nexwick (eager)",
    "cyanea",
    "phylo-nexus",
    "ncl",
    "ape",
    "BEAST2",
    "commonnexus",
    "DendroPy (lazy)",
    "DendroPy (eager)",
    "Biopython",
]


def classify_command(command: str) -> str:
    """Map a raw hyperfine command string to a human-readable parser name."""
    c = command.lower()
    if "nexwick" in c:
        return "nexwick (lazy)" if "--lazy" in c else "nexwick (eager)"
    if "cyanea" in c:
        return "cyanea"
    if "phylo_nexus" in c:
        return "phylo-nexus"
    if "ncl_harness" in c:
        return "ncl"
    if "parse_ape" in c:
        return "ape"
    if "beast2harness" in c:
        return "BEAST2"
    if "commonnexus" in c:
        return "commonnexus"
    if "dendropy_lazy" in c:
        return "DendroPy (lazy)"
    if "dendropy" in c:  # plain dendropy harness == eager mode
        return "DendroPy (eager)"
    if "biopython" in c:
        return "Biopython"
    return command  # fall back to the raw command if unrecognised


# --- reading ----------------------------------------------------------------

def _split_row(line: str) -> list[str]:
    """Split a markdown table row into non-empty cells.

    Dropping empty cells also repairs the stray extra ``|`` in the Biopython
    row of results_RSV2.md, which would otherwise shift every column.
    """
    cells = (c.strip().strip("`").strip() for c in line.strip().strip("|").split("|"))
    return [c for c in cells if c != ""]


def _parse_pm(cell: str) -> tuple[float, float]:
    """Parse a ``value ± std`` cell into (value, std); std defaults to 0."""
    parts = cell.split("±")
    value = float(parts[0].strip())
    std = float(parts[1].strip()) if len(parts) > 1 else 0.0
    return value, std


def _is_separator(cells: list[str]) -> bool:
    return all(set(c) <= set("-:") for c in cells)


def read_results_file(path: Path) -> pd.DataFrame:
    """Parse a single results_<dataset>.md into a tidy DataFrame."""
    dataset = DATASET_NAMES.get(
        path.stem.removeprefix("results_"), path.stem.removeprefix("results_")
    )

    unit_ms = 1.0
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = _split_row(line)
        if not cells or _is_separator(cells):
            continue
        if cells[0].lower() == "command":  # header row: read the time unit
            unit = re.search(r"\[(\w+)\]", cells[1])
            unit_ms = UNIT_TO_MS[unit.group(1)] if unit else 1.0
            continue

        command, mean_cell, _min_cell, _max_cell, rel_cell = cells
        mean, mean_std = _parse_pm(mean_cell)
        rel, rel_std = _parse_pm(rel_cell)
        records.append(
            {
                "dataset": dataset,
                "parser": classify_command(command),
                "mean_ms": mean * unit_ms,
                "std_ms": mean_std * unit_ms,
                "relative": rel,
                "relative_std": rel_std,
            }
        )
    return pd.DataFrame.from_records(records)


def read_all_results(results_dir: Path = RESULTS_DIR) -> pd.DataFrame:
    """Read every results_*.md file into one tidy long-form DataFrame."""
    frames = [read_results_file(p) for p in sorted(results_dir.glob("results_*.md"))]
    df = pd.concat(frames, ignore_index=True)
    df["parser"] = pd.Categorical(df["parser"], categories=PARSER_ORDER, ordered=True)
    return df.sort_values(["dataset", "parser"]).reset_index(drop=True)


# --- plotting ---------------------------------------------------------------

def _present_parsers(df: pd.DataFrame) -> list[str]:
    """Parsers that actually appear in the data, in PARSER_ORDER."""
    return [p for p in PARSER_ORDER if p in set(df["parser"])]


def plot_relative_grouped(df: pd.DataFrame, out_path: Path) -> None:
    """Grouped bars of relative slowdown per parser, one bar per dataset.

    Log y-axis because the slowdowns span 1x to ~150x. Error bars show the
    relative standard deviation, i.e. run-to-run variance.
    """
    parsers = _present_parsers(df)
    datasets = sorted(df["dataset"].unique())
    x = np.arange(len(parsers))
    width = 0.8 / len(datasets)

    fig, ax = plt.subplots(figsize=(12, 6))
    for i, ds in enumerate(datasets):
        sub = df[df["dataset"] == ds].set_index("parser").reindex(parsers)
        ax.bar(
            x + i * width,
            sub["relative"],
            width,
            yerr=sub["relative_std"],
            capsize=2,
            label=ds,
        )

    ax.set_yscale("log")
    ax.set_ylabel("Slowdown relative to fastest (x, log scale)")
    ax.set_title("Nexus parser slowdown relative to nexwick, by dataset")
    ax.set_xticks(x + width * (len(datasets) - 1) / 2)
    ax.set_xticklabels(parsers, rotation=30, ha="right")
    ax.axhline(1.0, color="grey", linewidth=0.8, linestyle="--")
    ax.legend(title="dataset")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_relative_fast(df: pd.DataFrame, out_path: Path, threshold: float = 6.0) -> None:
    """Zoom in on the close race among the fast parsers (linear scale).

    Only parsers whose slowdown stays under ``threshold`` on every dataset are
    shown, so the small differences at the top are readable. Error bars are the
    relative standard deviation.
    """
    fast = [
        p
        for p in _present_parsers(df)
        if df.loc[df["parser"] == p, "relative"].max() < threshold
    ]
    sub = df[df["parser"].isin(fast)]
    datasets = sorted(sub["dataset"].unique())
    x = np.arange(len(fast))
    width = 0.8 / len(datasets)

    fig, ax = plt.subplots(figsize=(9, 5))
    for i, ds in enumerate(datasets):
        d = sub[sub["dataset"] == ds].set_index("parser").reindex(fast)
        ax.bar(
            x + i * width,
            d["relative"],
            width,
            yerr=d["relative_std"],
            capsize=3,
            label=ds,
        )

    ax.set_ylabel("Slowdown relative to fastest (x)")
    ax.set_title(f"Fast parsers (< {threshold:g}x), by dataset")
    ax.set_xticks(x + width * (len(datasets) - 1) / 2)
    ax.set_xticklabels(fast, rotation=20, ha="right")
    ax.axhline(1.0, color="grey", linewidth=0.8, linestyle="--")
    ax.legend(title="dataset")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_relative_heatmap(df: pd.DataFrame, out_path: Path) -> None:
    """Heatmap of relative slowdown (parser x dataset), annotated with values.

    A compact overview that handles missing combinations (e.g. phylo-nexus,
    which only ran on RSV2) as blank cells.
    """
    table = df.pivot_table(index="parser", columns="dataset", values="relative", observed=True)
    table = table.reindex(_present_parsers(df))

    fig, ax = plt.subplots(figsize=(8, 6))
    data = np.ma.masked_invalid(table.to_numpy())
    im = ax.imshow(data, aspect="auto", cmap="YlOrRd", norm="log")

    ax.set_xticks(range(len(table.columns)), table.columns)
    ax.set_yticks(range(len(table.index)), table.index)
    for r in range(table.shape[0]):
        for c in range(table.shape[1]):
            v = table.iat[r, c]
            if not np.isnan(v):
                ax.text(c, r, f"{v:.1f}", ha="center", va="center", fontsize=8)

    ax.set_title("Slowdown relative to nexwick (x)")
    fig.colorbar(im, ax=ax, label="slowdown (x, log scale)")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def main() -> None:
    df = read_all_results()
    PLOTS_DIR.mkdir(exist_ok=True)
    plot_relative_grouped(df, PLOTS_DIR / "relative_grouped.png")
    plot_relative_fast(df, PLOTS_DIR / "relative_fast.png")
    plot_relative_heatmap(df, PLOTS_DIR / "relative_heatmap.png")
    print(f"Read {len(df)} rows across {df['dataset'].nunique()} datasets.")
    print(f"Wrote plots to {PLOTS_DIR}")


if __name__ == "__main__":
    main()