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

# Email alert config
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
ALERT_EMAIL = "harsh_singh@srmap.edu.in"  # Change if needed

def check_escalation(message_history: list[str], sentiment_history: list[str], return_reason=False):
    """
    Checks whether escalation is needed based on sentiment and keywords.
    Returns True or (True, reason) if return_reason=True.
    """
    if not message_history or not sentiment_history:
        return (False, None) if return_reason else False


    # Keyword-based escalation
    escalation_keywords = ["angry", "cancel", "complain", "worst", "useless", "frustrated", "refund"]
    last_message = message_history[-1].lower()

    if any(word in last_message for word in escalation_keywords):
        reason = "Trigger keyword detected"
        log_and_warn(message_history[-1], reason=reason)
        return (True, reason) if return_reason else True

    return (False, None) if return_reason else False

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
