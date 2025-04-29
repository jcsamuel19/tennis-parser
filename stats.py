"""Compute tennis stats from a list[Point]."""

from __future__ import annotations

import pandas as pd
from typing import List, Iterable
from lexer_parser import Point


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def _ensure_iter(points: Iterable[Point] | Point) -> list[Point]:
    """Accept a single Point or any iterable of Point objects."""
    if isinstance(points, Point):
        return [points]
    return list(points)


def compute_dataframe(points: Iterable[Point] | Point) -> pd.DataFrame:
    """Return a tidy DataFrame (one row per point)."""
    pts = _ensure_iter(points)
    if not pts:
        return pd.DataFrame(columns=["player", "outcome", "shot", "location"])

    # Convert NamedTuple → dict so pandas assigns column names automatically
    return pd.DataFrame([p._asdict() for p in pts]).fillna("")


def summary_table(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    counts = df.groupby(["player", "outcome"]).size().unstack(fill_value=0)
    counts["TOTAL"] = counts.sum(axis=1)
    return counts.reset_index()


def ace_df_ratio(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    df2 = df.query("outcome in ['ACE','DF']")
    pivot = df2.groupby(["player", "outcome"]).size().unstack(fill_value=0)
    pivot["ACE/DF"] = pivot["ACE"].div(pivot["DF"].replace(0, pd.NA))
    return pivot.reset_index()


def compute_all(points: Iterable[Point] | Point) -> dict[str, pd.DataFrame]:
    df = compute_dataframe(points)
    return {
        "raw": df,
        "by_outcome": summary_table(df),
        "ace_df": ace_df_ratio(df),
    }
