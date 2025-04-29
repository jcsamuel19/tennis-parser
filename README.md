# MatchNote → Stats Dashboard

A mini‑language, parser, and HTML generator that turns a compact tennis match log into an interactive statistics dashboard.

## 1 Project Structure
📁 src/
│   ├── lexer_parser.py      
│   ├── grammar.ebnf         
│   ├── stats.py             
│   ├── report.py            
│   ├── demo.txt             
📁 demo_output/              # Auto‑generated when you run the demo
│   ├── report.html
│   ├── bar.png
│   └── parse_tree.png        # Only if --tree flag is passed
requirements.txt
README.md ← this file

## 2 Setup

1 — Clone / unzip the repo
cd project‑root

2 — Create a clean venv (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

3 — Install dependencies
pip install -r requirements.txt

## 3  Quick‑start demo
python report.py demo.txt --tree  
open demo_output/report.html  

What happens

1. lexer_parser.py reads grammar.ebnf, builds an LALR parser, and transforms the log into a list of Point objects.
2. stats.py turns that list into tidy data‑frames (overall counts, ACE/DF ratio, …).
3. report.py renders those frames into an HTML dashboard with an embedded bar chart.

Where to look

1. demo_output/report.html → open in your browser to view the dashboard.

## 5  Design notes & assumptions

| Aspect  | Decision |
| ------------- | ------------- |
| Players | Always P1 / P2 (singles only). |
| Outcomes | ACE, DF, WINNER, ERROR. Validation handled by grammar.  |
| Optional fields | Content Cell  |
| Line endings | Content Cell  |
| Parsing strategy | Content Cell  |
| Outcomes | Content Cell  |
| Outcomes | Content Cell  |


Enjoy grading! 🎾