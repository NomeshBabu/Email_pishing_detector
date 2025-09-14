import joblib
import sys

# Load trained model & vectorizer
model = joblib.load("models/rf_model.pkl")
vectorizer = joblib.load("models/rf_vectorizer.pkl")

def predict_email(subject: str, sender: str, body: str):
    """Predict if an email is phishing or legitimate, with probabilities"""
    combined_text = f"Subject: {subject}\nFrom: {sender}\nBody: {body}"
    text_vec = vectorizer.transform([combined_text])
    prediction = model.predict(text_vec)[0]
    probs = model.predict_proba(text_vec)[0]  # [prob_legit, prob_phishing]

    legit_prob = probs[0]
    phish_prob = probs[1]

    if prediction == 1:
        label = "🚨 Phishing Email detected"
    else:
        label = "✅ Legitimate Email"

    return label, legit_prob, phish_prob


if __name__ == "__main__":
    print("🔍 Phishing Email Detector")
    print("Type 'exit' anytime to quit.\n")

    while True:
        # Ask separately
        subject = input("📌 Enter Subject: ").strip()
        if subject.lower() in ["exit", "quit", "q"]:
            print("👋 Exiting...")
            sys.exit(0)

        sender = input("✉️ Enter Sender (From): ").strip()
        if sender.lower() in ["exit", "quit", "q"]:
            print("👋 Exiting...")
            sys.exit(0)

        print("📝 Enter Body (finish with an empty line, or type 'exit' to quit):")
        body_lines = []
        while True:
            line = sys.stdin.readline().strip()
            if not line:
                break
            if line.lower() in ["exit", "quit", "q"]:
                print("👋 Exiting...")
                sys.exit(0)
            body_lines.append(line)

        body = " ".join(body_lines)

        # Run prediction
        label, legit_prob, phish_prob = predict_email(subject, sender, body)

        print("\nPrediction:", label)
        print(f"   ✅ Legitimate Probability: {legit_prob:.2f}")
        print(f"   🚨 Phishing Probability:   {phish_prob:.2f}")
        print("-" * 60)
