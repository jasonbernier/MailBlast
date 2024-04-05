#MailBlast.py
#Written by Jason Bernier
#https://github.com/jasonbernier/MailBlast

import sys
import smtplib
import ssl
import threading
import os
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import getpass

# Setup command-line argument parsing
parser = argparse.ArgumentParser(description="Send an email with an optional attachment.")
parser.add_argument("-s", "--server", help="SMTP server address.")
parser.add_argument("-p", "--port", type=int, default=587, help="SMTP server port, default is 587.")
parser.add_argument("-l", "--login", help="Login email for SMTP server.")
parser.add_argument("-f", "--from-email", help="From email address.")
parser.add_argument("-n", "--from-name", help="Name to display in the 'From' field (optional).")
parser.add_argument("-t", "--subject", help="Email subject.")
parser.add_argument("-b", "--body", help="Email body.")
parser.add_argument("-a", "--attachment", help="Path to attachment file.")
parser.add_argument("-r", "--recipients", help="Comma-separated list of recipient emails.")
args = parser.parse_args()

# Function to ensure mandatory input is provided, either via arguments or prompt
def get_mandatory_input(arg_value, prompt):
    if arg_value:
        return arg_value
    else:
        return input(prompt)

# Ensuring all required inputs are provided
smtp_server = get_mandatory_input(args.server, "Enter SMTP server: ")
login_email = get_mandatory_input(args.login, "Enter login email for SMTP server: ")
email_password = getpass.getpass("Enter your email password: ")
from_email = get_mandatory_input(args.from_email, "Enter 'From' email address: ")
from_name = args.from_name if args.from_name else from_email
subject = get_mandatory_input(args.subject, "Enter email subject: ")
body = get_mandatory_input(args.body, "Enter email body: ")
recipients_input = get_mandatory_input(args.recipients, "Enter recipient emails (comma-separated): ")
recipients = [email.strip() for email in recipients_input.split(',') if email.strip()]

# Handling attachment
attachment_path = args.attachment if args.attachment and os.path.isfile(args.attachment) else ""

# Function to construct and send an email
def send_email(recipient, smtp_server, port, login_email, sender_password, from_email, from_name, subject, body, attachment_path):
    print(f"Preparing to send email to {recipient}...")
    msg = MIMEMultipart()
    msg['From'] = f"{from_name} <{from_email}>"
    msg['To'] = recipient
    msg['Subject'] = subject

    # Attaching the email body
    msg.attach(MIMEText(body, 'plain'))

    # Attaching a file, if provided
    if attachment_path:
        print(f"Attaching file: {attachment_path}")
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(attachment_path)}")
        msg.attach(part)

    # Bypassing SSL certificate verification for development or troubleshooting
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    # Send the email via SMTP with TLS and error handling
    try:
        print(f"Connecting to SMTP server {smtp_server} on port {port}...")
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            print("TLS encryption started.")
            print("Authenticating with SMTP server...")
            server.login(login_email, sender_password)
            print("Authentication successful.")
            server.send_message(msg)
            print(f"Email successfully sent to {recipient}.")
    except smtplib.SMTPAuthenticationError:
        print("Failed to send email due to authentication error. Please check the username and password.")
        sys.exit()  # Exiting the script in case of authentication failure

# Function to initiate multi-threaded email sending
def threaded_sending():
    threads = []
    print("Starting to send emails...")
    for recipient in recipients:
        thread = threading.Thread(target=send_email, args=(recipient, smtp_server, args.port, login_email, email_password, from_email, from_name, subject, body, attachment_path))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All emails have been sent successfully.")

# Start the process
threaded_sending()
