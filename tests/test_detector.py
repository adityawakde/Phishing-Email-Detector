"""
test_detector.py
-----------------
Unit tests for the core detection logic in phishing_detector/detector.py.

Run with: pytest
"""

import pytest

from phishing_detector.detector import (
    count_keyword_hits,
    count_pattern_hits,
    calculate_phishing_score,
    classify_score,
    analyze_email,
)


# ----------------------------------------------------------------------
# count_keyword_hits()
# ----------------------------------------------------------------------

def test_count_keyword_hits_finds_known_phrase():
    """A single known phrase should be detected with its correct weight."""
    hits = count_keyword_hits("please verify account now")
    assert hits == {"verify account": 4}


def test_count_keyword_hits_multiple_phrases():
    """Multiple distinct phrases in the same text should all be found."""
    hits = count_keyword_hits("urgent: click here to reset password")
    assert hits == {"urgent": 2, "click here": 3, "password": 3}


def test_count_keyword_hits_no_match_returns_empty_dict():
    """Clean text with no suspicious phrases should return an empty dict."""
    hits = count_keyword_hits("hi, just checking in about lunch tomorrow")
    assert hits == {}


def test_count_keyword_hits_is_case_sensitive_to_input():
    """
    count_keyword_hits() does plain substring matching, so it relies on
    the caller (analyze_email) to lowercase text first. This test
    documents that behavior explicitly.
    """
    hits = count_keyword_hits("URGENT MESSAGE")  # uppercase, not pre-lowered
    assert hits == {}  # no match because phrase dict keys are lowercase


# ----------------------------------------------------------------------
# count_pattern_hits()
# ----------------------------------------------------------------------

def test_count_pattern_hits_detects_ip_link():
    """A raw IP-based URL should match the IP-link pattern."""
    hits = count_pattern_hits("Login at http://192.168.1.1/secure")
    assert any("d{1,3}" in pattern for pattern in hits)


def test_count_pattern_hits_detects_shortened_url():
    """A bit.ly shortened link should be flagged."""
    hits = count_pattern_hits("Claim your prize: bit.ly/abc123")
    # Dict keys are the raw regex strings (e.g. r"bit\.ly|..."), so we
    # check for the escaped form rather than the plain substring.
    assert any(r"bit\.ly" in pattern for pattern in hits)


def test_count_pattern_hits_no_match_returns_empty_dict():
    """Text with no URLs or prize language should return an empty dict."""
    hits = count_pattern_hits("See you at the meeting tomorrow.")
    assert hits == {}


# ----------------------------------------------------------------------
# calculate_phishing_score()
# ----------------------------------------------------------------------

def test_calculate_phishing_score_sums_weights():
    """Score should be the sum of all keyword and pattern weights."""
    keyword_hits = {"urgent": 2, "password": 3}
    pattern_hits = {"bit.ly": 3}
    assert calculate_phishing_score(keyword_hits, pattern_hits) == 8


def test_calculate_phishing_score_handles_empty_inputs():
    """No hits at all should produce a score of zero."""
    assert calculate_phishing_score({}, {}) == 0


# ----------------------------------------------------------------------
# classify_score()
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "score,expected_label",
    [
        (0, "Safe"),
        (2, "Safe"),
        (3, "Suspicious"),
        (6, "Suspicious"),
        (7, "Highly Suspicious"),
        (20, "Highly Suspicious"),
    ],
)
def test_classify_score_boundaries(score, expected_label):
    """Verify classification at and around each threshold boundary."""
    assert classify_score(score) == expected_label


# ----------------------------------------------------------------------
# analyze_email() — integration-style tests of the full pipeline
# ----------------------------------------------------------------------

def test_analyze_email_safe_text():
    """Ordinary, harmless text should classify as Safe."""
    result = analyze_email("Hey, are we still meeting for coffee at 10am?")
    assert result["classification"] == "Safe"
    assert result["score"] == 0


def test_analyze_email_highly_suspicious_text():
    """Text packed with strong phishing signals should be Highly Suspicious."""
    text = (
        "URGENT: Your account has been suspended. "
        "Click here to verify account and confirm your identity "
        "by logging in immediately."
    )
    result = analyze_email(text)
    assert result["classification"] == "Highly Suspicious"
    assert result["score"] >= 7


def test_analyze_email_is_case_insensitive_for_keywords():
    """
    analyze_email() lowercases input before keyword matching, so
    uppercase phishing text should still be detected (unlike calling
    count_keyword_hits() directly on raw text).
    """
    result = analyze_email("URGENT! VERIFY ACCOUNT NOW")
    assert "urgent" in result["keyword_hits"]
    assert "verify account" in result["keyword_hits"]


def test_analyze_email_empty_string():
    """An empty string should be Safe with a score of zero, not an error."""
    result = analyze_email("")
    assert result["score"] == 0
    assert result["classification"] == "Safe"


def test_analyze_email_rejects_non_string_input():
    """Passing a non-string type should raise a clear TypeError."""
    with pytest.raises(TypeError):
        analyze_email(12345)


def test_analyze_email_result_has_expected_keys():
    """The result dict should always contain exactly these four keys."""
    result = analyze_email("hello world")
    assert set(result.keys()) == {
        "keyword_hits",
        "pattern_hits",
        "score",
        "classification",
    }
