import logging
from colorama import init, Fore, Style
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize colorama
init(autoreset=True)

# Setup logging
logging.basicConfig(
    filename="escalation_log.txt",
    level=logging.INFO,
    format="%(asctime)s - ESCALATION - %(message)s"
)

# Email alert config (set these in .env)
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
ALERT_EMAIL = "harsh_singh@srmap.edu.in"  # You can change this if needed

def check_escalation(message_history: list[str], sentiment_history: list[str]) -> bool:
    """
    Checks whether escalation is needed based on sentiment and keywords.
    Returns True if triggered. Also logs and sends alerts.
    """
    # Count recent 'very negative' sentiments
    negative_count = sum(1 for s in sentiment_history[-3:] if "very negative" in s)

    if negative_count >= 2:
        log_and_warn(message_history[-1], reason="Repeated very negative sentiment")
        return True

    # Keyword-based escalation
    escalation_keywords = ["angry", "cancel", "complain", "worst", "useless", "frustrated", "refund"]
    last_message = message_history[-1].lower()

    if any(word in last_message for word in escalation_keywords):
        log_and_warn(message_history[-1], reason="Trigger keyword detected")
        return True

    return False

def log_and_warn(message: str, reason: str):
    """
    Logs escalation, shows CLI warning, and sends email alert.
    """
    logging.info(f"Escalation triggered due to: {reason} | Message: {message}")

    # Console alerts
    print(Fore.YELLOW + Style.BRIGHT + "\n⚠️ Escalation Alert: This conversation may need human intervention!")
    print(Fore.CYAN + f"Reason: {reason}\n")
    print(Fore.MAGENTA + "[Simulated Alert] Escalation log saved. (Check escalation_log.txt)")

    # Email notification
    send_email_alert(reason, message)

def send_email_alert(reason, message):
    """
    Sends escalation alert via email using Gmail SMTP.
    """
    subject = "🚨 Escalation Detected in RAG Support Assistant"
    body = f"""
    <h3>Escalation Triggered</h3>
    <p><strong>Reason:</strong> {reason}</p>
    <p><strong>User Message:</strong> {message}</p>
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = ALERT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        print("📧 Escalation email sent successfully.")
    except Exception as e:
        print(Fore.RED + f"❌ Failed to send email: {e}")
