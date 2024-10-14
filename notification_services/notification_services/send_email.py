import email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from fastapi import HTTPException 

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "hasaanqureshi150@gmail.com"
SENDER_PASSWORD = "hq@~/|..*&9197436"


def send_email(to_email : str , subject : str , message : str):
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # create Email 

        email_message = MIMEMultipart()
        email_message["From"] = SENDER_EMAIL
        email_message["To"] = to_email
        email_message["Subject"] = subject
        email_message.attach(MIMEText(message, "plain"))


        ### Send Email

        server.sendmail(SENDER_EMAIL, to_email , email_message.as_string)
        server.quit()
        print(f"Email sent to {to_email} with Subject: {subject}")
    except Exception as e:
        print(f"Error sending email to {to_email}: {str(e)}")
        raise HTTPException(status_code=500 , detail="Failed to send Email")