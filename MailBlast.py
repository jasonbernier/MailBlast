#MailBlast.py
#Written by Jason Bernier
#https://github.com/jasonbernier/MailBlast

import sys
import smtplib
import ssl
import threading
import os
import argparse
import tkinter as tk
from tkinter import scrolledtext, ttk, filedialog, Toplevel
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import getpass
from tkhtmlview import HTMLLabel
from tkinterhtml import HtmlFrame

class MailBlastApp:
    def __init__(self, master):
        self.master = master
        master.title("MailBlast")
        self.setup_ui()

    def setup_ui(self):
        row = 0
        ttk.Label(self.master, text="From Email:").grid(row=row, sticky="e")
        self.from_email = ttk.Entry(self.master)
        self.from_email.grid(row=row, column=1, sticky="ew")
        row += 1

        ttk.Label(self.master, text="From Name:").grid(row=row, sticky="e")
        self.from_name = ttk.Entry(self.master)
        self.from_name.grid(row=row, column=1, sticky="ew")
        row += 1

        ttk.Label(self.master, text="SMTP Server(s):").grid(row=row, sticky="e")
        self.smtp_server = ttk.Entry(self.master)
        self.smtp_server.grid(row=row, column=1, sticky="ew")
        row += 1

        ttk.Label(self.master, text="SMTP Port:").grid(row=row, sticky="e")
        self.smtp_port = ttk.Entry(self.master)
        self.smtp_port.insert(0, "587")
        self.smtp_port.grid(row=row, column=1, sticky="ew")
        row += 1

        ttk.Label(self.master, text="SMTP Login:").grid(row=row, sticky="e")
        self.smtp_login = ttk.Entry(self.master)
        self.smtp_login.grid(row=row, column=1, sticky="ew")
        row += 1

        ttk.Label(self.master, text="SMTP Password:").grid(row=row, sticky="e")
        self.smtp_password = ttk.Entry(self.master, show="*")
        self.smtp_password.grid(row=row, column=1, sticky="ew")
        row += 1

        ttk.Label(self.master, text="To (Recipients):").grid(row=row, sticky="e")
        self.to_email = ttk.Entry(self.master)
        self.to_email.grid(row=row, column=1, sticky="ew")
        row += 1

        ttk.Label(self.master, text="Subject:").grid(row=row, sticky="e")
        self.subject = ttk.Entry(self.master)
        self.subject.grid(row=row, column=1, sticky="ew")
        row += 1

        ttk.Label(self.master, text="Body:").grid(row=row, sticky="ne")
        self.body = scrolledtext.ScrolledText(self.master, height=10)
        self.body.grid(row=row, column=1, sticky="ew")
        row += 1

        self.attach_btn = ttk.Button(self.master, text="Attach File", command=self.attach_file)
        self.attach_btn.grid(row=row, column=0, sticky="ew")
        self.remove_attach_btn = ttk.Button(self.master, text="Remove Attachment", command=self.remove_attachment)
        self.remove_attach_btn.grid(row=row, column=1, sticky="ew")
        self.load_template_btn = ttk.Button(self.master, text="Load Template", command=self.load_template)
        self.load_template_btn.grid(row=row, column=2, sticky="ew")
        self.preview_btn = ttk.Button(self.master, text="Preview Email", command=self.preview_email)
        self.preview_btn.grid(row=row, column=3, sticky="ew")
        row += 1

        self.send_btn = ttk.Button(self.master, text="Send", command=self.retrieve_and_send)
        self.send_btn.grid(row=row, column=0, columnspan=4, sticky="ew")
        row += 1

        self.status_text = scrolledtext.ScrolledText(self.master, height=5)
        self.status_text.grid(row=row, column=0, columnspan=4, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.status_text.yview)
        scrollbar.grid(row=0, column=5, rowspan=row, sticky="ns")
        self.status_text.config(yscrollcommand=scrollbar.set)

        for i in range(row + 1):
            self.master.grid_rowconfigure(i, weight=1)
        for i in range(6):
            self.master.grid_columnconfigure(i, weight=1)

    def attach_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.attachment = filename

    def remove_attachment(self):
        if hasattr(self, 'attachment'):
            delattr(self, 'attachment')

    def load_template(self):
        filename = filedialog.askopenfilename()
        if filename:
            with open(filename, "r") as file:
                template = file.read()
            self.body.delete("1.0", tk.END)
            self.body.insert(tk.END, template)

    def preview_email(self):
        from_email = self.from_email.get()
        from_name = self.from_name.get()
        to_email = self.to_email.get()
        subject = self.subject.get()
        body = self.body.get("1.0", tk.END).strip()

        html = f"<html><body><h1>{subject}</h1><p>{body}</p></body></html>"

        preview_window = Toplevel(self.master)
        preview_window.title("Email Preview")
        try:
            email_preview = HTMLLabel(preview_window, html=html)
            email_preview.pack(expand=True, fill=tk.BOTH)
            self.html_preview = email_preview
        except:
            email_preview = HtmlFrame(preview_window, horizontal_scrollbar="auto")
            email_preview.pack(expand=True, fill=tk.BOTH)
            email_preview.set_content(html)
            self.html_preview = email_preview

    def retrieve_and_send(self):
        from_email = self.from_email.get()
        from_name = self.from_name.get()
        smtp_server = self.smtp_server.get()
        smtp_port = int(self.smtp_port.get())
        smtp_login = self.smtp_login.get()
        smtp_password = self.smtp_password.get()
        to_email = self.to_email.get()
        subject = self.subject.get()
        body = self.body.get("1.0", tk.END).strip()
        attachment = self.attachment if hasattr(self, 'attachment') else None

        if not (from_email and from_name and smtp_server and smtp_port and smtp_login and smtp_password and to_email and subject and body):
            self.show_status("Please fill in all fields.")
            return

        threading.Thread(target=self.send_emails, args=(from_email, from_name, smtp_server, smtp_port, smtp_login, smtp_password, to_email, subject, body, attachment)).start()

    def send_emails(self, from_email, from_name, smtp_server, smtp_port, smtp_login, smtp_password, to_email, subject, body, attachment):
        try:
            smtp = smtplib.SMTP(smtp_server, smtp_port)
            smtp.starttls()
            smtp.login(smtp_login, smtp_password)

            msg = MIMEMultipart()
            msg['From'] = f"{from_name} <{from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject

            if attachment:
                attachment_data = self.load_attachment(attachment)
                msg.attach(attachment_data)

            if not (body.startswith("<html>") and body.endswith("</html>")):
                body = f"<html>{body}</html>"
                
            msg.attach(MIMEText(body, 'html'))

            smtp.send_message(msg)
            smtp.quit()

            self.show_status(f"Email successfully sent to {to_email} via {smtp_server}")
        except Exception as e:
            self.show_status(f"Failed to send email: {str(e)}")

    def load_attachment(self, attachment):
        with open(attachment, "rb") as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {attachment.split("/")[-1]}')
        return part

    def show_status(self, message):
        if self.master:
            self.master.after(0, self._update_status, message)

    def _update_status(self, message):
        self.status_text.insert(tk.END, message + '\n')
        self.status_text.see(tk.END)

def send_email_command_line(args):
    smtp_server = get_mandatory_input(args.server, "Enter SMTP server: ")
    login_email = get_mandatory_input(args.login, "Enter login email for SMTP server: ")
    email_password = args.password if args.password else getpass.getpass("Enter your email password: ")
    from_email = get_mandatory_input(args.from_email, "Enter 'From' email address: ")
    from_name = args.from_name if args.from_name else from_email
    subject = get_mandatory_input(args.subject, "Enter email subject: ")
    body = get_mandatory_input(args.body, "Enter email body: ")
    recipients_input = get_mandatory_input(args.recipients, "Enter recipient emails (comma-separated): ")
    recipients = [email.strip() for email in recipients_input.split(',') if email.strip()]

    attachment_path = args.attachment if args.attachment and os.path.isfile(args.attachment) else ""

    if not (body.startswith("<html>") and body.endswith("</html>")):
        body = f"<html>{body}</html>"

    def send_email(recipient, smtp_server, port, login_email, sender_password, from_email, from_name, subject, body, attachment_path):
        print(f"Preparing to send email to {recipient}...")
        msg = MIMEMultipart()
        msg['From'] = f"{from_name} <{from_email}>"
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        if attachment_path:
            print(f"Attaching file: {attachment_path}")
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(attachment_path)}")
            msg.attach(part)

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

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
            sys.exit()

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

    threaded_sending()

def get_mandatory_input(arg_value, prompt):
    if arg_value:
        return arg_value
    else:
        return input(prompt)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send an email with an optional attachment.")
    parser.add_argument("-g", "--gui", action="store_true", help="Run the GUI version of MailBlast.")
    parser.add_argument("-s", "--server", help="SMTP server address.")
    parser.add_argument("-p", "--port", type=int, default=587, help="SMTP server port, default is 587.")
    parser.add_argument("-l", "--login", help="Login email for SMTP server.")
    parser.add_argument("-f", "--from-email", help="From email address.")
    parser.add_argument("-n", "--from-name", help="Name to display in the 'From' field (optional).")
    parser.add_argument("-t", "--subject", help="Email subject.")
    parser.add_argument("-b", "--body", help="Email body.")
    parser.add_argument("-a", "--attachment", help="Path to attachment file.")
    parser.add_argument("-r", "--recipients", help="Comma-separated list of recipient emails.")
    parser.add_argument("-pw", "--password", help="SMTP password.")
    args = parser.parse_args()

    if args.gui:
        root = tk.Tk()
        app = MailBlastApp(root)
        root.mainloop()
    else:
        send_email_command_line(args)
