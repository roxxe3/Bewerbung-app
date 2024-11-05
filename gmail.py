import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from flask import Flask, request, render_template, jsonify
from data import (
    Anwendungsentwicklung,
    Systemintegration,
    Daten_und_Prozessanalyse,
    Digitale_Vernetzung,
    Mathematisch_technischer_Softwareentwickler
)
import os
from quickstart import append_data

app = Flask(__name__)
app.config['password'] = os.getenv('password')

# Dictionary mapping each ausbildung option to its details
AUSBILDUNG_OPTIONS = {
    "Anwendungsentwicklung": Anwendungsentwicklung,
    "Systemintegration": Systemintegration,
    "Daten- und Prozessanalyse": Daten_und_Prozessanalyse,
    "digitale Vernetzung": Digitale_Vernetzung,
    "Mathematisch technischer Softwareentwickler": Mathematisch_technischer_Softwareentwickler
}



def send_email_with_attachments(smtp_server, port, sender_email, receiver_email, password, subject, body, file_paths):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    for file_path in file_paths:
        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {file_path.split('/')[-1]}")
        message.attach(part)

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form.get('email')
    ausbildung = request.form.get('ausbildung')

    ausbildung_details = AUSBILDUNG_OPTIONS.get(ausbildung)
    if ausbildung_details:
        send_email_with_attachments(
            smtp_server="smtp.gmail.com",
            port=587,
            sender_email="hamzafarissi@gmail.com",
            receiver_email=email,
            password=app.config['password'],
            subject=ausbildung_details["subject"],
            body=ausbildung_details["body"],
            file_paths=ausbildung_details["file_paths"]
        )
        append_data(ausbildung, email)
        return jsonify({"status": "success", "message": f"Email sent to {email} for {ausbildung}"})
    else:
        return jsonify({"status": "error", "message": "Invalid ausbildung option"}), 400

if __name__ == '__main__':
    app.run(debug=True)
