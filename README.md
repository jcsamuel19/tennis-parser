# MatchNote → Stats Dashboard

A mini‑language, parser, and HTML generator that turns a compact tennis match log into an interactive statistics dashboard.
The goal is to parse MatchNote logs — tiny, human-typed “score sheets” that record one tennis point per line.
## 1. Project Structure
```
src/
├── lexer_parser.py       # Lark grammar + transformer → Point list
├── grammar.ebnf          # BNF/EBNF description of the MatchNote DSL
├── stats.py              # Computes pandas data‑frames & quick plots
├── report.py             # CLI – parse → stats → HTML (and PNGs)
└── templates/
    └── report.html.jinja

demo_input/
└── demo.txt              # 10‑point sample log used in the walk‑through

demo_output/              # Auto‑generated when you run the demo
├── report.html
├── bar.png
└── parse_tree.png        # Only if --tree flag is passed

requirements.txt
README.md                 
```
## 2. Setup

1 — Clone / unzip the repo
```
cd project‑root
```

2 — Create a clean venv (optional but recommended)
```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3 — Install dependencies
```
pip install -r requirements.txt
```
## 3. Quick‑start demo
```
python report.py demo.txt  
open demo_output/report.html  
```
## 4. Step by step flow:
<img width="686" alt="Screenshot 2025-04-29 at 7 21 19 PM" src="https://github.com/user-attachments/assets/919dd73f-c928-4e12-934e-66724575a651" />


## 5. File Overview


### 1. What a raw file looks like 


```
# Demo.txt

P1: ACE T
P2: DF
P1: WINNER FH CC
P2: ERROR BH DL
```
Each line says:

| Field  | Example | Meaning |
| ------------- | ------------- |------------- |
| player | P1 | Who served / hit the final shot (P1 or P2) |
| outcome | ACE | Point result (ACE, DF, WINNER, ERROR) |
| shot | FH | Optional – stroke type (FH forehand / BH backhand) |
| location | CC | Optional – ball placement (CC cross-court, DL down-the-line, T, WIDE) |




### 2. Grammar overview
```
# grammar.ebnf

match        : point_line+
point_line   : player ':' outcome shot? location? NEWLINE
player       : "P1" | "P2"
outcome      : "ACE" | "DF" | "WINNER" | "ERROR"
shot         : "FH" | "BH"
location     : "CC" | "DL" | "T" | "WIDE"
```

| Rule | What it matches | Example line(s) | Notes |
| ---         |     ---      |          --- | --- |
| `match`| One or more point_line entries (greedy +). Allows an entire log to be parsed in a single call. | (whole file) | The outermost rule; no delimiters other than newlines. |
|`point_line`| A single point of play: player ':' outcome plus optional shot and optional location, followed by a newline. | P1: WINNER FH CC | Using optionals keeps the DSL compact—e.g., a double‑fault needs only "P2: DF". |
| `player` | Literal P1 or P2. | P2 | Keeps the language singles‑only and avoids name parsing. |
| `outcome` | Literal ACE, DF, WINNER, or ERROR. | ACE | Parsed as the primary event so downstream stats pivot on this field. |
| `shot` | Forehand/backhand abbreviations FH or BH. | FH | Provides extra context for winners/errors but is not required for serves or double faults. |
| `location` | Court‑location shorthand: CC (cross‑court), DL (down‑the‑line), T, WIDE. | CC | Location is only meaningful when shot is present; the grammar does not enforce that relationship to keep parsing simple. |

### 3. What the parser does
- Lexer + grammar (in `grammar.ebnf`) recognize the tokens above.

- Lark feeds the parse tree through a custom `Transformer`, turning each line into a `Point(player, outcome, shot, location)` named-tuple.

- You receive a Python list of `Point` objects – a clean, structured dataset that downstream code (`stats.py`) can group, count, and plot.

**Parsing order:** Because Lark’s default lexer is regex‑based and unambiguously tokenises literals, the grammar remains LL(1)/LALR‑friendly. Each optional is right‑growing—so ambiguous inputs like P1: ACE WIDE still parse correctly (WIDE becomes location).

**Parse Tree:**
```
match
 ├── point_line
 │   ├── player    P1
 │   ├── outcome   ACE
 │   └── location  T
 ├── point_line
 │   ├── player    P2
 │   └── outcome   DF
 └── point_line
     ├── player    P1
     ├── outcome   WINNER
     ├── shot      FH
     └── location  CC
```
### 4. Why parse at all?

Parsing converts that free-form text into structured data once, so everything after—statistics, HTML tables, bar charts—becomes a few pandas operations.

So, when you run:
```
python src/report.py demo_input/demo.txt
```
you are really asking:

“Read the MatchNote log, parse every line into machine-readable Points, then use those to build my stats dashboard.”


## 7. Troubleshooting

| Symptom | Fix |
| -- | -- |
| `graphviz` missing → no `parse_tree.png` | `brew install graphviz` or `apt-get install graphviz`. |
| Matplotlib complains about GUI backend | The script selects the non‑GUI "Agg" backend automatically. |


## 8. Outputs
<img width="679" alt="Screenshot 2025-04-29 at 8 34 40 PM" src="https://github.com/user-attachments/assets/0c67b476-2450-4758-864f-08ddb6075fd0" />

<img width="1438" alt="Screenshot 2025-04-29 at 8 33 54 PM" src="https://github.com/user-attachments/assets/04bc42c2-e3c3-45fd-ba73-9ee61ed3904f" />


Enjoy! 🎾
