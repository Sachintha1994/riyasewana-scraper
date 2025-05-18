import smtplib
from email.mime.text import MIMEText

GMAIL_USER = "sachinthathilina@gmail.com"
GMAIL_PASS = "cohy uubp mydy kmuc"

def send_email(ads, subject, to):
    body = ""
    for ad in ads:
        body += f"🚗 {ad['title']}\n"
        body += f"📍 {ad['location']} | 📅 {ad['date']} | 🛣️ {ad['mileage']}\n"
        body += f"💰 {ad['price']}\n"
        body += f"🔗 {ad['link']}\n\n"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = GMAIL_USER
    msg['To'] = to

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_PASS)
        smtp.send_message(msg)
        print(f"✅ Email sent to {to} with {len(ads)} new ads.")
