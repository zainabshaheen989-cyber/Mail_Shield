def text_score(text):

    text = text.lower()

    spam_score = 0
    promo_score = 0
    ml_adjust = 0

    # =====================
    # SAFE KEYWORDS (HARD SAFE SIGNAL)
    # =====================
    safe_keywords = [
        "meeting", "report", "update", "project",
        "team", "conference", "minutes", "agenda"
    ]

    if any(word in text for word in safe_keywords):
        return -2, ml_adjust, 0   # SAFE SIGNAL

    # =====================
    # SPAM SIGNALS (ONLY PHISHING RISK)
    # =====================
    spam_patterns = [
        "urgent", "verify", "otp", "password",
        "account blocked", "click now", "immediately",
        "security alert", "login required"
    ]

    for p in spam_patterns:
        if p in text:
            spam_score += 1.5

    if "win" in text and "prize" in text:
        spam_score += 2

    if "act now" in text:
        spam_score += 1.5

    if text.count("!") > 3:
        spam_score += 1

    # =====================
    # PROMOTIONAL SIGNALS (NO SPAM LINK)
    # =====================
    promo_patterns = [
        "discount", "sale", "offer", "deal",
        "buy now", "save", "coupon",
        "limited time offer", "special offer",
        "flat", "cashback"
    ]

    for p in promo_patterns:
        if p in text:
            promo_score += 1.5

    # =====================
    # FINAL OUTPUT (SEPARATED LOGIC)
    # =====================
    return min(spam_score, 7), ml_adjust, min(promo_score, 7)