from flask import Flask, render_template, request
import pickle

from core.source_check import source_score
from core.text_nlp import text_score
from core.link_analyzer import link_score
from core.brand_checker import brand_score

app = Flask(__name__)

model = pickle.load(open("ml/model.pkl", "rb"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    email = request.form["email"].lower()

    # =====================
    # FEATURE SCORES
    # =====================
    s = source_score(email)
    t, ml_adjust, promo_score = text_score(email)
    l = link_score(email)
    b = brand_score(email)

    # =====================
    # ML MODEL
    # =====================
    ml_pred = model.predict([email])[0]

    ml_score = 4 if ml_pred == 1 else 0

    # =====================
    # FINAL SCORE ENGINE
    # =====================
    final_score = (
        (s * 0.8) +
        (t * 0.5) +
        (l * 1.2) +
        (b * 1.0) +
        (ml_score * 1.5) +
        ml_adjust +
        (promo_score * 0.3)
    )

    # =====================
    # STRONG SPAM DETECTION
    # =====================
    is_spam = False

    if ml_pred == 1:
        is_spam = True
    elif l >= 4:
        is_spam = True
    elif s >= 5:
        is_spam = True
    elif final_score > 8:
        is_spam = True

    # =====================
    # FINAL RESULT
    # =====================
    if is_spam:
        result = "SPAM (🚨 PHISHING EMAIL)"
        ml_label = "SUSPICIOUS"

    elif promo_score > 0:
        result = "HAM (📢 PROMOTIONAL EMAIL)"
        ml_label = "PROMOTIONAL"

    else:
        result = "HAM (✅ SAFE EMAIL)"
        ml_label = "NORMAL"

    # =====================
    # WARNING
    # =====================
    warning = ""
    if is_spam:
        warning = "⚠️ This email looks dangerous. Do not click links."

    return render_template(
        "index.html",
        prediction=result,
        score=round(final_score, 2),
        source=round(s, 2),
        text=round(t, 2),
        link=round(l, 2),
        brand=round(b, 2),
        ml=ml_label,
        warning=warning
    )


if __name__ == "__main__":
    app.run(debug=True)