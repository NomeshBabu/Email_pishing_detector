# main.py
from detector.engine import detect_email

if __name__ == "__main__":
    print("=== Phishing Email Detector ===")

    subject = input("Enter email subject: ")
    body = input("Enter email body: ")
    from_addr = input("Enter sender email address: ")

    verdict, reasons = detect_email(subject, body, from_addr)

    print("\n--- Detection Result ---")
    if verdict:
        print("⚠️  This email looks like PHISHING (Spam)")
    else:
        print("✅ This email looks SAFE (Ham)")

    if reasons:
        print("\nReasons:")
        for r in reasons:
            print(" -", r)



