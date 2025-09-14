import joblib
import os

MODEL_PATH = os.path.join("models", "phishing_model.pkl")

# Load trained model
if not os.path.exists(MODEL_PATH):
    print("❌ Model not found! Please run train_model.py first.")
    exit()

model = joblib.load(MODEL_PATH)

# Some sample test messages
test_messages = [
    "Hey, are we still meeting for lunch tomorrow?",  # Ham
    "URGENT! Your account has been compromised. Click here to reset your password.",  # Phishing
    "Don't miss out on this limited-time offer!!!",  # Spam/Phishing
    "Your subscription has been renewed successfully",  # Ham
]

print("=== Model Test ===")
for msg in test_messages:
    prob = model.predict_proba([msg])[0][1]   # Probability of spam/phishing
    pred = "Phishing/Spam" if prob > 0.5 else "Ham (Safe)"
    print(f"\nMessage: {msg}")
    print(f"Prediction: {pred}")
    print(f"Probability (phishing): {prob:.2f}")
