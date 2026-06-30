from phishing_detector.detector import analyze_email
from ml_model.predict import predict_email
from ml_model.header_analyzer import analyze_headers
from ml_model.email_parser import parse_email


def hybrid_analyze(text: str):

    parsed = parse_email(text)
    body = parsed["body"]

    rule_result = analyze_email(body)
    ml_result = predict_email(body)
    header_result = analyze_headers(text)

    risk = rule_result["score"] + (ml_result["confidence"] / 20)

    if header_result["domain_spoof"] or "unknown" in parsed["headers"].get("from", ""):
        risk += 5

    return {
        "final_verdict": "HIGHLY SUSPICIOUS" if risk > 8 else "SAFE",
        "hybrid_score": round(risk, 2),
        "headers": parsed["headers"],
        "ml": ml_result,
        "rules": rule_result
    }