# test_model_improved.py
import joblib, os

MODEL_PATH = os.path.join("models", "phishing_model.pkl")
if not os.path.exists(MODEL_PATH):
    print("Model not found. Run train_model_improved.py first.")
    exit()

model = joblib.load(MODEL_PATH)

tests = [
    "Hey, are we still meeting for lunch tomorrow?",
    "URGENT! Your account has been compromised. Click here to reset your password.",
    "Don't miss out on this limited-time offer!!!",
    "Your subscription has been renewed successfully"
]

for msg in tests:
    prob = model.predict_proba([msg])[0][1]
    label = "Phishing/Spam" if prob > 0.5 else "Ham (Safe)"
    print("\nMessage:", msg)
    print("Probability (phishing):", f"{prob:.2f}", "=>", label)
