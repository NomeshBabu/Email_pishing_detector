# detector/ml.py
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

MODEL_PATH = os.path.join("models", "phish_model.pkl")
VEC_PATH = os.path.join("models", "tfidf.pkl")

# You can adjust this threshold (default 0.3 = more sensitive to phishing)
PHISH_THRESHOLD = 0.3

def load_datasets(data_folder="data"):
    """Load and combine multiple CSV datasets into one DataFrame."""
    all_data = []
    for file in os.listdir(data_folder):
        if file.endswith(".csv"):
            path = os.path.join(data_folder, file)
            try:
                df = pd.read_csv(path)
                # Normalize columns
                if "text" not in df.columns:
                    for c in df.columns:
                        if "email" in c.lower() or "message" in c.lower() or "content" in c.lower() or "body" in c.lower():
                            df = df.rename(columns={c: "text"})
                if "label" not in df.columns:
                    for c in df.columns:
                        if "phish" in c.lower() or "spam" in c.lower() or "class" in c.lower() or "target" in c.lower():
                            df = df.rename(columns={c: "label"})
                if "text" in df.columns and "label" in df.columns:
                    all_data.append(df[["text", "label"]])
            except Exception as e:
                print(f"Skipping {file}: {e}")
    return pd.concat(all_data, ignore_index=True)


def train_model():
    """Train a TF-IDF + Logistic Regression model with balanced classes."""
    df = load_datasets()
    print(f"Loaded {len(df)} emails from datasets")

    # Clean data
    df = df.dropna()
    df["text"] = df["text"].astype(str)

    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["label"], test_size=0.2, random_state=42
    )

    # TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Logistic Regression with balanced classes
    model = LogisticRegression(max_iter=300, class_weight="balanced")
    model.fit(X_train_tfidf, y_train)

    # Evaluate
    preds = model.predict(X_test_tfidf)
    print(classification_report(y_test, preds))

    # Save model + vectorizer
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VEC_PATH)
    print("✅ Model trained and saved!")


# detector/ml.py
def predict_ml(subject: str, body: str):
    """
    Placeholder for ML-based detection.
    Later we will replace this with a trained model.
    For now it always returns (False, 0.0).
    """
    return False, 0.0


