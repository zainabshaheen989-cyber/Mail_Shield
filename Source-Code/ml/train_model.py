import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

df1 = pd.read_csv("data/dataset.csv", encoding="utf-8", engine="python", on_bad_lines="skip")
df2 = pd.read_csv("data/spam.csv", encoding="latin-1", engine="python", on_bad_lines="skip")

df2 = df2.rename(columns={"v1": "label", "v2": "text"})
df2 = df2[["label", "text"]]
df = pd.concat([df1, df2], ignore_index=True)

df = df[["label", "text"]].dropna()
df["text"] = df["text"].astype(str)

# remove junk rows
df = df[df["text"].str.len() > 5]
df["label"] = df["label"].map({"spam": 1, "ham": 0})

X = df["text"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = Pipeline([
    ("tfidf", TfidfVectorizer(
        stop_words="english",
        max_features=8000,
        min_df=1,
        max_df=0.95
    )),
    ("clf", LogisticRegression(max_iter=1000))
])

model.fit(X_train, y_train)

pickle.dump(model, open("ml/model.pkl", "wb"))

print("Model trained successfully")
