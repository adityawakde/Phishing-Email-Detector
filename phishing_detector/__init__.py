"""
phishing_detector package
--------------------------
A rule-based phishing email detector.

Public API:
    analyze_email(text: str) -> dict

Example:
    >>> from phishing_detector import analyze_email
    >>> result = analyze_email("Urgent! Click here to verify account")
    >>> result["classification"]
    'Highly Suspicious'
"""

from phishing_detector.detector import analyze_email

__all__ = ["analyze_email"]
__version__ = "0.1.0"
