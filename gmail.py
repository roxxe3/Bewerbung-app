import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
# app.py
from flask import Flask, request, render_template
from data import Anwendungsentwicklung

app = Flask(__name__)

def send_email_with_attachments(smtp_server, port, sender_email, receiver_email, password, subject, body, file_paths):
    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Add body to email
    message.attach(MIMEText(body, 'plain'))

    # Attach each file
    for file_path in file_paths:
        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {file_path.split('/')[-1]}")
        message.attach(part)

    # Send the email
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Capture the form data

    email = request.form.get('email')
    ausbildung = request.form.get('ausbildung')
    print(ausbildung)
    
    # You can now process the data, save it, or send it back
    if ausbildung == "Anwendungsentwicklung":
        send_email_with_attachments(
        smtp_server="smtp.gmail.com",
        port=587,
        sender_email="hamzafarissi@gmail.com",
        receiver_email= email,
        password="sawv qtvi fgvk cuza",
        subject=Anwendungsentwicklung["subject"],
        body=Anwendungsentwicklung["body"],
        file_paths=Anwendungsentwicklung["file_paths"]
        )
    return f"Email - {email}"

# Usage
# email = input("enter receiver email: ")
# email_type = input("select aus: ")
# print("1-  Anwendungsentwicklung")
# print("2-  Daten- und Prozessanalyse")
# print("3-  Systemintegration")
# print("4 - digitale Vernetzung")
# print("...")

# if email_type == 1:
#     send_email_with_attachments(
#     smtp_server="smtp.gmail.com",
#     port=587,
#     sender_email="hamzafarissi@gmail.com",
#     receiver_email= email,
#     password="sawv qtvi fgvk cuza",
#     subject="Bewerbung Ausbildung Fachinformatikar Anwendungsentwicklung 2025",
#     body="""
#         Sehr geehrte Damen und Herren,

#         mit großer Begeisterung habe ich mich soeben auf eine Ausbildungsstelle als Fachinformatiker Anwendungsentwicklung für 2025 beworben. Anbei sende ich Ihnen noch mein Anschreiben und meinen Lebenslauf. Ich freue mich auf eine Rückmeldung von Ihnen.

#         Mit freundlichen Grüßen,

#         Hamza Farissi""",
#     file_paths=["lebenslauf.pdf"]
#     )
if __name__ == '__main__':
    app.run(debug=True)