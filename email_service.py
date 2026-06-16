import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

def send_otp_email(receiver_email, otp):

    msg = MIMEText(
        f"""
Hello,

Your verification code is:

{otp}

Please enter this OTP to verify your email.

Regards,
SwiftIntelli Team
"""
    )

    msg["Subject"] = "Email Verification"
    msg["From"] = EMAIL
    msg["To"] = receiver_email

    with smtplib.SMTP_SSL(
        SMTP_HOST,
        SMTP_PORT
    ) as server:

        server.login(
            EMAIL,
            PASSWORD
        )

        server.send_message(msg)