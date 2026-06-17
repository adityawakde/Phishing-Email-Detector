"""
detector.py
-----------
Core phishing detection logic.

IMPORTANT DESIGN RULE: nothing in this file calls input() or print().
It only takes strings in and returns data structures out. This keeps
the logic reusable from anywhere — a CLI, a Flask API (Phase 2), a
test suite, or a batch script — without any rewriting.
"""

import re


# ----------------------------------------------------------------------
# Keyword/phrase database
# ----------------------------------------------------------------------
# Each suspicious phrase has a weight reflecting how strong an indicator
# it is. Stronger phishing signals (e.g. "verify account") score higher
# than mild ones (e.g. "urgent").
SUSPICIOUS_PHRASES = {
    "urgent": 2,
    "verify account": 4,
    "click here": 3,
    "password": 3,
    "bank": 2,
    "login immediately": 4,
    "confirm your identity": 4,
    "suspended": 3,
    "act now": 3,
    "limited time": 2,
    "social security": 4,
    "wire transfer": 4,
}

# Patterns that often appear in phishing emails (regex-based, not just
# plain substrings) — e.g. IP-based links or shortened URLs.
SUSPICIOUS_PATTERNS = {
    r"http[s]?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}": 4,  # raw IP links
    r"bit\.ly|tinyurl\.com|t\.co": 3,                      # shortened URLs
    r"\$\d+[,\d]*\s*(reward|prize|won)": 3,                # fake prize/money
}


def count_keyword_hits(text: str) -> dict:
    """
    Scan text for known suspicious phrases.

    Why a function: isolating this logic makes it easy to test, reuse,
    or swap out the keyword list later without touching scoring logic.

    Parameters:
        text (str): The lowercased email body to scan.

    Returns:
        dict: A mapping of {phrase: weight} for every phrase found.
              Returning the matches (not just a score) lets the caller
              show *why* something was flagged.
    """
    found = {}
    for phrase, weight in SUSPICIOUS_PHRASES.items():
        if phrase in text:
            found[phrase] = weight
    return found


def count_pattern_hits(text: str) -> dict:
    """
    Scan text for suspicious regex patterns (e.g. IP-based links, URL
    shorteners, fake prize amounts).

    Why a function: regex matching is logically different from plain
    keyword matching, so separating it keeps each function doing one
    clear job (single-responsibility principle).

    Parameters:
        text (str): The email body to scan (original case preserved).

    Returns:
        dict: A mapping of {pattern: weight} for every pattern matched.
    """
    found = {}
    for pattern, weight in SUSPICIOUS_PATTERNS.items():
        if re.search(pattern, text, re.IGNORECASE):
            found[pattern] = weight
    return found


def calculate_phishing_score(keyword_hits: dict, pattern_hits: dict) -> int:
    """
    Sum the weights of all matched phrases and patterns into a single
    numeric phishing score.

    Why a function: separating "what matched" from "how much it's worth
    in total" makes the scoring rule easy to change later without
    touching the detection logic above.

    Parameters:
        keyword_hits (dict): Output of count_keyword_hits().
        pattern_hits (dict): Output of count_pattern_hits().

    Returns:
        int: Total phishing score.
    """
    return sum(keyword_hits.values()) + sum(pattern_hits.values())


def classify_score(score: int) -> str:
    """
    Convert a numeric phishing score into a human-readable risk label.

    Thresholds (tunable):
        0-2   -> Safe
        3-6   -> Suspicious
        7+    -> Highly Suspicious

    Why a function: keeping thresholds in one place means you only
    need to edit this function to recalibrate sensitivity.

    Parameters:
        score (int): Total phishing score.

    Returns:
        str: One of "Safe", "Suspicious", "Highly Suspicious".
    """
    if score <= 2:
        return "Safe"
    elif score <= 6:
        return "Suspicious"
    else:
        return "Highly Suspicious"


def analyze_email(text: str) -> dict:
    """
    Run the full detection pipeline on a piece of email text.

    This is the single public function that other code (CLI now, an
    API later) should call. It ties together keyword detection,
    pattern detection, scoring, and classification.

    Parameters:
        text (str): Raw email text.

    Returns:
        dict: {
            "keyword_hits": {...},
            "pattern_hits": {...},
            "score": int,
            "classification": str
        }
    """
    if not isinstance(text, str):
        raise TypeError("analyze_email() expects a string")

    lowered = text.lower()  # keyword matching is case-insensitive
    keyword_hits = count_keyword_hits(lowered)
    pattern_hits = count_pattern_hits(text)  # patterns checked on original text
    score = calculate_phishing_score(keyword_hits, pattern_hits)
    classification = classify_score(score)

    return {
        "keyword_hits": keyword_hits,
        "pattern_hits": pattern_hits,
        "score": score,
        "classification": classification,
    }
