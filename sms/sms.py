# Imports for the twilio sms endpoint
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from pathlib import Path
import os
import json


num_sheet = Path(__file__).parent / "./data/num_sheet.json"

# Create sendgrid instance
sg = SendGridAPIClient(api_key=os.environ["SENDGRID_API_KEY"])


def email_lookup(num):
    with num_sheet.open() as data:
        """Looks up the email to be used from num_sheet.json
        Emails are stored in json format with the number being used as the key.
        Eg:
        {
        "1NXXNXXXXXX": "email@example.com",
        "+1NXXNXXXXXX": "email@example.com"
        }
        """
        num_dict = json.load(data)
        to_email = {value for (key, value) in num_dict.items() if str(num) == key}
        try:
            return to_email.pop()
        except KeyError:
            return False


def send_email(to_email, txt_from, txt_to, txt_body):
    """Send an email using SendGrid."""
    mail = Mail(
        from_email=f"{txt_from}@berthfield.com",
        to_emails=f"{to_email}",
        subject=f'SMS from {txt_from} for {txt_to}.',
        html_content=f'{txt_body}'
    )

    try:
        response = sg.send(mail)
        print(response.status_code, response.body, response.headers)
        return response.status_code
    except Exception as e:
        print(e.messages)