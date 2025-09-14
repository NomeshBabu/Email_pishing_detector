# train_model_improved.py
import os
import glob
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# ---------- Config ----------
DATA_FOLDER = "data"
MODEL_FOLDER = "models"
os.makedirs(MODEL_FOLDER, exist_ok=True)

# columns to look for
TEXT_CANDIDATES = ["text", "body", "message", "content", "Text", "subject", "text_combined"]
LABEL_CANDIDATES = ["label", "Type", "target", "class", "Category", "is_phish"]

# mapping strings -> 0/1
LABEL_MAP = {
    # ham / legit -> 0
    "ham": 0, "legit": 0, "good": 0, "benign": 0, "non-spam": 0, "not spam": 0,
    "safe": 0, "false": 0, "no": 0, "n": 0, "0": 0, "0.0": 0, "false": 0,
    # spam/phish -> 1
    "spam": 1, "phish": 1, "phishing": 1, "fraud": 1, "scam": 1, "malicious": 1,
    "attack": 1, "1": 1, "1.0": 1, "true": 1, "yes": 1, "y": 1
}

# ---------- Load CSVs ----------
csv_files = glob.glob(os.path.join(DATA_FOLDER, "*.csv"))
if not csv_files:
    raise FileNotFoundError(f"No CSV files found in folder '{DATA_FOLDER}'")

all_dfs = []
print("📂 Loading CSV files...")
for fpath in csv_files:
    fname = os.path.basename(fpath)
    try:
        df = pd.read_csv(fpath, low_memory=False, encoding="utf-8", dtype=object)
    except Exception as e:
        print(f"⚠️ Skipping {fname}: failed to read ({e})")
        continue

    # find text column
    text_col = next((c for c in TEXT_CANDIDATES if c in df.columns), None)
    label_col = next((c for c in LABEL_CANDIDATES if c in df.columns), None)

    if text_col is None or label_col is None:
        print(f"⚠️ Skipping {fname} (no text/label column found)")
        continue

    # extract columns
    subset = df[[text_col, label_col]].dropna(how="all").copy()
    subset = subset.rename(columns={text_col: "text", label_col: "label"})

    # normalize text
    subset["text"] = subset["text"].astype(str).fillna("").str.strip()

    # normalize label: try string mapping first
    # convert to string, lower, strip
    subset["label_raw"] = subset["label"].astype(str).str.lower().str.strip()

    # map strings
    subset["label_mapped"] = subset["label_raw"].map(LABEL_MAP)

    # if still null, try numeric conversion (some files use numerical labels)
    mask_null = subset["label_mapped"].isna()
    if mask_null.any():
        numeric = pd.to_numeric(subset.loc[mask_null, "label_raw"], errors="coerce")
        subset.loc[mask_null, "label_mapped"] = numeric.where(numeric.isin([0, 1]), other=pd.NA)

    # drop rows where mapping failed
    subset = subset.dropna(subset=["label_mapped", "text"])
    if subset.empty:
        print(f"⚠️ Skipping {fname} (no rows with valid labels after normalization)")
        continue

    # convert to int labels
    subset["label"] = subset["label_mapped"].astype(int)
    subset = subset[["text", "label"]]

    print(f"✅ Loaded {fname} -> {len(subset)} usable rows")
    all_dfs.append(subset)

# combine
if not all_dfs:
    raise ValueError("❌ No usable data found across CSV files.")
df_all = pd.concat(all_dfs, ignore_index=True)
print(f"\n✅ Total usable rows combined: {len(df_all)}")
print("Label counts:\n", df_all["label"].value_counts())

# ---------- Train/Test split ----------
X = df_all["text"].astype(str).values
y = df_all["label"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# ---------- Vectorize ----------
vectorizer = TfidfVectorizer(ngram_range=(1,2), stop_words="english", max_features=50000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# ---------- Train RandomForest ----------
print("\n🚀 Training RandomForestClassifier...")
rf = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)
rf.fit(X_train_vec, y_train)

# ---------- Evaluate ----------
y_pred = rf.predict(X_test_vec)
print("\n📊 Evaluation results:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# ---------- Save model & vectorizer ----------
joblib.dump(rf, os.path.join(MODEL_FOLDER, "rf_model.pkl"))
joblib.dump(vectorizer, os.path.join(MODEL_FOLDER, "rf_vectorizer.pkl"))
print(f"\n✅ Saved rf_model.pkl and rf_vectorizer.pkl into '{MODEL_FOLDER}/'")





