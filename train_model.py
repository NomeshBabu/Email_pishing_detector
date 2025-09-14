import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Load dataset (tab separated)
df = pd.read_csv("data/SMSSpamCollection", sep="\t", names=["label", "message"])

# Convert labels: ham → 0, spam → 1
df["label"] = df["label"].map({"ham": 0, "spam": 1})

# Features and labels
X = df["message"]
y = df["label"]

# Create TF-IDF + Logistic Regression pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english")),
    ("clf", LogisticRegression(max_iter=1000))
])

# Train the model
model.fit(X, y)

# Save model
joblib.dump(model, "models/phishing_model.pkl")
print("✅ Model trained on SMS dataset and saved to models/phishing_model.pkl")
