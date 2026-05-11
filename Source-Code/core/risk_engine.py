def compute_final_risk(score):

    if score <= 2:
        return "HAM (✅SAFE EMAIL)"
    elif score <= 5:
        return "HAM (📢 PROMOTIONAL EMAIL)"
    else:
        return "SPAM(🚨 PHISHING EMAIL)"