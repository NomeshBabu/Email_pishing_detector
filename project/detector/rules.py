# detector/rules.py
import re
import tldextract

# Common suspicious words in phishing
SUSPICIOUS_WORDS = {
    "urgent", "verify", "account", "password", "reset",
    "confirm", "click", "limited", "invoice", "bank"
}

# Known shortener domains
SHORTENERS = {"bit.ly", "goo.gl", "t.co", "tinyurl.com", "ow.ly", "is.gd", "buff.ly"}


def extract_urls(text: str):
    """Extract URLs from text using regex."""
    return re.findall(r'https?://[^\s)>\]"\']+', text, flags=re.I)


def url_features(url: str):
    """Check suspicious patterns in URLs."""
    ext = tldextract.extract(url)
    domain = f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain
    has_ip = bool(re.match(r'https?://(\d{1,3}\.){3}\d{1,3}', url))
    many_subs = len(ext.subdomain.split(".")) >= 3 if ext.subdomain else False
    at_symbol = "@" in url
    suspicious_path = any(x in url.lower() for x in ["login", "verify", "update", "secure", "confirm"])
    shortener = domain in SHORTENERS

    return {
        "has_ip": has_ip,
        "many_subs": many_subs,
        "at_symbol": at_symbol,
        "suspicious_path": suspicious_path,
        "shortener": shortener,
        "domain": domain,
    }


def check_rules(subject: str, body: str, from_addr: str):
    """
    Apply rule-based phishing checks.
    Returns (is_suspicious: bool, reasons: list).
    """
    text = f"{subject} {body}".lower()
    reasons = []

    # Keyword check
    for word in SUSPICIOUS_WORDS:
        if word in text:
            reasons.append(f"Suspicious word found: '{word}'")

    # URL check
    urls = extract_urls(text)
    for url in urls:
        feats = url_features(url)
        if feats["has_ip"]:
            reasons.append(f"URL uses raw IP: {url}")
        if feats["many_subs"]:
            reasons.append(f"URL has many subdomains: {url}")
        if feats["at_symbol"]:
            reasons.append(f"URL contains @ symbol: {url}")
        if feats["suspicious_path"]:
            reasons.append(f"Suspicious path in URL: {url}")
        if feats["shortener"]:
            reasons.append(f"URL uses shortener ({feats['domain']}): {url}")

    # Sender vs content mismatch (simple check)
    if from_addr.split("@")[-1] not in text and urls:
        reasons.append("Sender domain not mentioned in body but links present")

    return (len(reasons) > 0), reasons
