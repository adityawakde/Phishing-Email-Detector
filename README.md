# Phishing Email Detector

A rule-based tool that scans email text for common phishing indicators
and classifies the result as **Safe**, **Suspicious**, or **Highly
Suspicious**.

> **Status:** Phase 1 — core detection logic + CLI. Not a production
> spam filter; this is a heuristic/educational tool. Real-world
> defenses should also check sender authentication (SPF/DKIM/DMARC),
> URL reputation, and ideally a trained ML model.

## Project Roadmap

- **Phase 1 (current):** Installable package, core detection logic
  separated from I/O, CLI entry point, unit tests.
- **Phase 2 (planned):** Flask/FastAPI web service exposing
  `analyze_email()` over HTTP.
- **Later phases:** ML-based scoring, expanded pattern detection
  (lookalike domains, link/text mismatches), persistence/logging.

## Project Structure

```
phishing-detector/
├── phishing_detector/
│   ├── __init__.py     # package entry point, exposes analyze_email()
│   ├── detector.py     # core detection logic (pure functions, no I/O)
│   └── cli.py           # console input/output only
├── tests/
│   └── test_detector.py
├── requirements.txt
├── setup.py
└── README.md
```

The detection logic in `detector.py` never calls `input()` or `print()`.
This is intentional: it's the seam that lets Phase 2 plug a web
framework in front of the same logic without rewriting it.

## Installation

```bash
# 1. Clone or navigate into the project folder
cd phishing-detector

# 2. (Recommended) create a virtual environment
python3 -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate

# 3. Install dev dependencies (pytest)
pip install -r requirements.txt

# 4. Install the package itself in editable mode
pip install -e .
```

## Usage

After installation, run the CLI tool:

```bash
phishing-detector
```

Or run it directly without installing:

```bash
python -m phishing_detector.cli
```

Paste your email text, then press Enter on a blank line to run the
analysis. Example:

```
=== Phishing Email Detector ===
Paste the email text below. Press Enter twice (blank line) when done:

URGENT: Your account has been suspended. Click here to verify account.


--- Phishing Detection Report ---

Suspicious phrases found:
  - 'urgent' (weight: 2)
  - 'verify account' (weight: 4)
  - 'click here' (weight: 3)
  - 'suspended' (weight: 3)

No suspicious URL/pattern indicators found.

Total Phishing Score: 12
Classification: Highly Suspicious
----------------------------------
```

You can also use it as a library, which is how Phase 2's web API will
call it:

```python
from phishing_detector import analyze_email

result = analyze_email("Click here to verify account immediately")
print(result["classification"])  # "Highly Suspicious"
```

## Testing

Run the unit test suite with:

```bash
pytest
```

For more detail:

```bash
pytest -v
```

Tests cover keyword matching, pattern matching, score calculation,
classification thresholds, and the full `analyze_email()` pipeline
(including edge cases: empty input, mixed case, non-string input).

## Scoring Logic (current thresholds)

| Score Range | Classification     |
|-------------|---------------------|
| 0 – 2       | Safe                 |
| 3 – 6       | Suspicious           |
| 7+          | Highly Suspicious    |

Thresholds and keyword weights live in `detector.py` and are easy to
retune as you collect more sample data.

## License

Educational project — license to be decided.
