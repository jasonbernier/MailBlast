# MailBlast

MailBlast is a Python application for sending emails with optional attachments. It provides both a graphical user interface (GUI) and a command-line interface (CLI) for sending emails. 

## Features

- GUI for easy email composition and sending.
- CLI for sending emails from the command line.
- Supports sending HTML emails.
- Option to attach files to emails.
- Supports templates
- Preview email before sending (GUI mode only).

## Installation

1. Clone the repository:

    ```
    git clone https://github.com/jasonbernier/MailBlast.git
    cd MailBlast
    ```

2. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

## Usage

### GUI

Run the GUI version of MailBlast using the following command:

    
    python mailblast.py -g
   
### CLI

Run the CLI version of MailBlast using the following command:

    
    python mailblast.py [options]
    

Replace `[options]` with the appropriate command-line options. Use the `-h` or `--help` option to see the available options.


Replace `[options]` with the appropriate command-line options. Use the `-h` or `--help` option to see the available options.

## Command-line Options

- `-s, --server`: SMTP server address.
- `-p, --port`: SMTP server port (default is 587).
- `-l, --login`: Login email for the SMTP server.
- `-f, --from-email`: From email address.
- `-n, --from-name`: Name to display in the 'From' field (optional).
- `-t, --subject`: Email subject.
- `-b, --body`: Email body.
- `-a, --attachment`: Path to attachment file.
- `-r, --recipients`: Comma-separated list of recipient emails.
- `-pw, --password`: SMTP password.

## Disclaimer

This script is provided for educational and testing purposes only. Use it responsibly and at your own risk. The author is not responsible for any misuse or damage caused by this script.





