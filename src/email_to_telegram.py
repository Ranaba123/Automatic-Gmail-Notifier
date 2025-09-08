import imaplib
import email
import requests
import os

# --- CONFIG FROM ENVIRONMENT VARIABLES ---
IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = os.environ.get("EMAIL_ACCOUNT")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# --- FUNCTIONS ---
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Telegram API error: {response.text}")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def check_inbox():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("inbox")

        result, data = mail.search(None, "UNSEEN")  # only new emails
        if result == "OK":
            for num in data[0].split():
                result, msg_data = mail.fetch(num, "(RFC822)")
                if result == "OK":
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    subject = msg["subject"]
                    from_ = msg["from"]

                    notify = f"📧 New Email\nFrom: {from_}\nSubject: {subject}"
                    send_telegram_message(notify)
        mail.logout()
    except Exception as e:
        print(f"Error checking inbox: {e}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    check_inbox()
