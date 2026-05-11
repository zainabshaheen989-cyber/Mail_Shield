import re

TRUSTED_DOMAINS = {"gmail.com", "amazon.com", "google.com", "microsoft.com"}
TRUSTED_BRANDS = ["amazon", "google", "microsoft","Daraz","foodpanda"]

def source_score(text):

    matches = re.findall(r'([\w\.-]+)@([\w\.-]+)', text)

    if not matches:
        return 3

    score = 0

    for username, domain in matches:
        domain = domain.lower()

        if domain not in TRUSTED_DOMAINS:
            score += 2

        for brand in TRUSTED_BRANDS:
            if brand in text.lower() and brand not in domain:
                score += 3

        if any(x in domain for x in ["secure", "verify", "login"]):
            score += 2

    return min(score, 5)