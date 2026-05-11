import re
import json

with open("data/blacklist_domains.json") as f:
    BLACKLIST = json.load(f)["blacklist"]

def link_score(text):

    score = 0
    links = re.findall(r'(https?://\S+)', text)

    for link in links:

        if "http://" in link:
            score += 1.5

        if any(x in link for x in ["bit.ly", "tinyurl"]):
            score += 2

        if any(x in link.lower() for x in ["login", "verify", "secure", "bank"]):
            score += 2.5

        for bad in BLACKLIST:
            if bad in link:
                score += 3

        if any(x in link for x in [".xyz", ".top", ".ru"]):
            score += 2

    return min(score, 8)