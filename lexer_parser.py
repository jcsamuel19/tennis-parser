"""Parse MatchNote DSL → list[Point] using Lark.
Run as script for quick inspection:
$ python lexer_parser.py demo.txt --tree
"""

from __future__ import annotations
from pathlib import Path
from typing import NamedTuple, Optional, List
from lark import Lark, Transformer, v_args


# ---------------------------------------------------------------------------
# Data Model
# ---------------------------------------------------------------------------
class Point(NamedTuple):
    """A single point in the match log."""

    player: str  # "P1" or "P2"
    outcome: str  # ACE / DF / WINNER / ERROR
    shot: Optional[str]
    location: Optional[str]


# ---------------------------------------------------------------------------
# Grammar & Parser
# ---------------------------------------------------------------------------
_GRAMMAR_PATH = Path(__file__).parent / "grammar.ebnf"
_GRAMMAR_TEXT = _GRAMMAR_PATH.read_text(encoding="utf-8")

# Lark instance is cheap to build; cache it at module import
_PARSER = Lark(
    _GRAMMAR_TEXT,
    parser="lalr",
    start="match",
    propagate_positions=False,
    maybe_placeholders=False,
    lexer="standard",
    keep_all_tokens=False,
)


@v_args(inline=True)
class _TreeToPoint(Transformer):
    """Convert Lark parse tree → Point objects."""

    def match(self, *points):
        return list(points)

    def player(self, tok):  # type: ignore[override]
        return str(tok)

    def outcome(self, tok):  # type: ignore[override]
        return str(tok)

    def shot(self, tok):  # type: ignore[override]
        return str(tok)

    def location(self, tok):  # type: ignore[override]
        return str(tok)

    def point_line(
        self,
        player: str,
        outcome: str,
        shot: Optional[str] | None = None,
        location: Optional[str] | None = None,
    ) -> Point:  # type: ignore[override]
        return Point(player, outcome, shot, location)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def parse(text: str) -> List[Point]:
    """Parse DSL string → list[Point]."""

    tree = _PARSER.parse(text)  # Ensure final EOL for last rule
    points: List[Point] = _TreeToPoint().transform(tree)  # type: ignore[arg-type]
    return points


def parse_file(path: str | Path) -> List[Point]:
    return parse(Path(path).read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# CLI helper
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse, pprint

    ap = argparse.ArgumentParser(description="Parse MatchNote log → list[Point]")
    ap.add_argument("file", help="Path to match log txt file")
    ap.add_argument("--tree", action="store_true", help="Print parse tree")
    args = ap.parse_args()

    raw = Path(args.file).read_text(encoding="utf-8")
    points = parse(raw)
    pprint.pp(points)

    if args.tree:
        tree = _PARSER.parse(raw + "")
        print(tree.pretty())
