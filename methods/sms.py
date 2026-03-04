# Imports for the twilio methods endpoint
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path
import json

num_sheet = Path(__file__).parent / "../data/num_sheet.json"

# Create sendgrid instance
# sg = SendGridAPIClient(api_key=os.environ["SENDGRID_API_KEY"])\

# --- Smtp Configuration ---

smtp_server = "smtp.email.us-ashburn-1.oci.oraclecloud.com"  # e.g., for Gmail, use 'smtp.gmail.com'
smtp_port = 587                 # 587 is the standard port for STARTTLS

# Use an app password if using Gmail
sender_email = "ocid1.user.oc1..aaaaaaaaarda64tfmanoxlil3syvukmejhtjuivojuyukdlbascaddtcup3q@ocid1.tenancy.oc1..aaaaaaaalrnb6nvn3nqhaof7wq6czzx2bzg7nkkpp3j2mw32frcihw55s2za.1r.com"
sender_password = "V2r>:mhzYU+;(M6:<q1v"
# receiver_email = "recipient_email@example.com"
# subject = "SMTP Email from Python"
# body = "This is a plain-text email sent from a Python script."

def email_lookup(num):
    """Looks up the email to be used from num_sheet.json.

    Emails are stored in json format with the number being used as the key.
    Eg:
    {
    "1NXXNXXXXXX": "email@example.com",
    "+1NXXNXXXXXX": "email@example.com"
    }
    """
    with num_sheet.open() as data:
        num_dict = json.load(data)
        # Use .get() for a direct, safe lookup. It returns None if the key is not found.
        return num_dict.get(str(num))


def send_email(to_email, txt_from, txt_to, txt_body):
    """Send an email using OCI SMTP."""
    # Create an EmailMessage object for a modern and safe way to build emails.
    emsg = EmailMessage()
    emsg["Subject"] = f'SMS from {txt_from} for {txt_to}'
    emsg["From"] = "noreply@berthfield.com"
    emsg["To"] = to_email
    emsg.set_content(txt_body)

    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)  # Secure the connection with TLS
            server.ehlo()  # Re-identify after starting TLS
            server.login(sender_email, sender_password)
            server.send_message(emsg)
            print("Email sent successfully!")

    except smtplib.SMTPException as e:
        print(f"Error: unable to send email. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
