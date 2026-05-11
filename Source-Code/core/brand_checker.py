import json

# =====================
# LOAD TRUSTED BRANDS
# =====================
with open("data/whitelist_brands.json", encoding="utf-8") as f:
    TRUSTED = json.load(f)["trusted_brands"]


def brand_score(text):

    text = text.lower()

    # =====================
    # STRONG SAFE SIGNAL (IMPORTANT FIX)
    # =====================
    for brand in TRUSTED:
        if brand.lower() in text:
            return -3   # strong SAFE signal (important improvement)

    # =====================
    # PROMOTIONAL SIGNALS (light weight only)
    # =====================
    promo_keywords = [
        "discount", "offer", "sale", "deal",
        "limited time", "cashback", "coupon"
    ]

    score = 0

    for p in promo_keywords:
        if p in text:
            score += 1

    # =====================
    # FINAL OUTPUT
    # =====================
    return min(score, 2)