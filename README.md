
# MailBlast
#Written by Jason Bernier

MailBlast is a versatile Python script for sending emails with optional attachments to multiple recipients efficiently. It's designed to work with any SMTP server and provides both command-line and interactive modes for ease of use.

## Features

- **Flexible SMTP Configuration**: Supports custom SMTP servers and ports.
- **Command-line & Interactive Modes**: Use command-line arguments for automation or prompts for manual input.
- **Optional Attachments**: Easily attach files to your emails.
- **Multi-Recipient Support**: Send emails to multiple recipients simultaneously with multi-threading.
- **SSL/TLS Encryption**: Ensures secure email transmission.

## Prerequisites

- Python 3.x
- Access to an SMTP server (with credentials)

## Setup

1. Clone this repository or download `MailBlast.py` to your local system.
   ```bash
   git clone https://github.com/jasonbernier/MailBlast.git
   ```
2. Ensure Python 3 is installed on your system.

## Usage

MailBlast can be run with command-line arguments for quick sending or without arguments to use the interactive mode which will prompt for details.

### Command-line Arguments

- `-s`, `--server`: SMTP server address (Required)
- `-p`, `--port`: SMTP server port, defaults to 587
- `-l`, `--login`: Login email for SMTP authentication (Required)
- `-f`, `--from-email`: 'From' email address (Required)
- `-n`, `--from-name`: Display name for the 'From' field (Optional)
- `-t`, `--subject`: Email subject (Required)
- `-b`, `--body`: Email body content (Required)
- `-a`, `--attachment`: File path for the email attachment (Optional)
- `-r`, `--recipients`: Comma-separated list of recipient emails (Required)

#### Example Command

```bash
python MailBlast.py -s smtp.example.com -p 587 -l your_email@example.com -f your_email@example.com -n "Your Name" -t "Subject Here" -b "Hello, World!" -a "/path/to/file.pdf" -r "recipient1@example.com,recipient2@example.com"
```

### Interactive Mode

Run `MailBlast.py` without any arguments to enter interactive mode, which will prompt you for all required details:

```bash
python MailBlast.py
```

## Security Note

MailBlast supports bypassing SSL certificate verification for development purposes. Use this feature cautiously and ensure secure handling of email credentials.

## Contributing

Contributions to MailBlast are welcome! Please refer to the contributing guidelines for more information.

