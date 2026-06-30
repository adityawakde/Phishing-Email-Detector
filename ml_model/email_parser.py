import re

def parse_email(raw_text: str):
    """
    Simulates real email parsing (headers + body separation)
    """

    headers = {}
    body = raw_text

    # Fake header extraction patterns
    if "from:" in raw_text.lower():
        match = re.search(r"from:\s*(.*)", raw_text, re.IGNORECASE)
        headers["from"] = match.group(1) if match else "unknown"

    if "reply-to:" in raw_text.lower():
        match = re.search(r"reply-to:\s*(.*)", raw_text, re.IGNORECASE)
        headers["reply-to"] = match.group(1) if match else "unknown"

    # Clean body (remove header-like lines)
    body = re.sub(r"from:.*|reply-to:.*", "", raw_text, flags=re.IGNORECASE)

    return {
        "headers": headers,
        "body": body.strip()
    }