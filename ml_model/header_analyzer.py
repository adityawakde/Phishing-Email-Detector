import re

def analyze_headers(email_text: str):
    """
    Simulated email header analysis.

    In real systems, headers come from email metadata.
    Here we simulate detection patterns.
    """

    result = {
        "spf_check": "pass",
        "dkim_check": "pass",
        "domain_spoof": False,
        "suspicious_sender": False
    }

    text = email_text.lower()

    # Fake domain spoof detection
    if "bank" in text and "gmail" in text:
        result["domain_spoof"] = True

    # Suspicious patterns
    if re.search(r"urgent|verify|password|login", text):
        result["suspicious_sender"] = True

    # Simulated failures
    if "http" in text or "click here" in text:
        result["spf_check"] = "fail"

    if "bit.ly" in text:
        result["dkim_check"] = "fail"

    return result