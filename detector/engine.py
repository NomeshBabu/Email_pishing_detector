# detector/engine.py
from detector.rules import check_rules
from detector.ml import predict_ml

def detect_email(subject: str, body: str, from_addr: str):
    reasons = []

    # Rule-based
    rule_flag, rule_reasons = check_rules(subject, body, from_addr)
    reasons.extend(rule_reasons)

    # ML-based
    ml_flag, ml_prob = predict_ml(subject, body)
    if ml_prob > 0:
        reasons.append(f"ML probability (phishing): {ml_prob:.2f}")

    # Fusion logic:
    # - if rules think it's suspicious → be more permissive with ML (lower threshold)
    # - otherwise use conservative threshold
    ml_threshold = 0.5
    if rule_flag:
        ml_threshold = 0.25   # lower threshold when heuristics already suspicious

    verdict = rule_flag or (ml_prob >= ml_threshold)
    return verdict, reasons




