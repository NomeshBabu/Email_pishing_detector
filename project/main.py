# main.py
from detector.engine import detect_email

if __name__ == "__main__":
    subject = "Urgent: Verify your account now"
    body = "Click this link http://bit.ly/fake-login to reset your password."
    from_addr = "support@bank-secure.com"

    verdict, reasons = detect_email(subject, body, from_addr)

    print("Phishing Detected?", verdict)
    print("Reasons:")
    for r in reasons:
        print(" -", r)
