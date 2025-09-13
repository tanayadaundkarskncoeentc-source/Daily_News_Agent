# email_utils
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def send_email(news_items):
    sender = os.environ.get("EMAIL_ADDRESS")
    password = os.environ.get("EMAIL_PASSWORD")

    recipients = [
        "tanayadaundkar31@gmail.com",
        # "ketan.mane@gurukulcode.com",
        # "rohini.satale@gurukulcode.com",
        # "balaji.wagh@gurukulcode.com",
        # "ashish.bakhade@gurukulcode.com",
        # "rohinimahatme3@gmail.com"
    ]

    subject = "📰 AI News"

    if not news_items:
        body = "No relevant AI news found in the last 24 hours."
    else:
        body = "\n\n".join([
            f"📢 Source: {item['source']}\n"
            f"📰 Title: {item['title']}\n"
            f"📅 Published: {item['published']}\n"
            f"📝 Summary: {item['summary']}\n"
            f"🔗 Read more: {item['link']}"
            for item in news_items
        ])

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, password)
            smtp.sendmail(sender, recipients, msg.as_string())
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
