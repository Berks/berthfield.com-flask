from flask import Flask, render_template, request
import os
import datetime
import json

# Imports for the twilio sms endpoint
import sendgrid
from sendgrid.helpers.mail import Mail
# from validate_email import validate_email

# Create sendgrid instance
sg = sendgrid.SendGridAPIClient(api_key=os.environ["SENDGRID_API_KEY"])
# Create flask instance
app = Flask(__name__)

# Set attribute to mitigate error in dev environ... Not sure of the root cause
app.__name__ = "__main__"
app.name = "Berthfield Server"

# Get formatted date for the index template.
date = datetime.datetime.now()
formatted_date = date.strftime("%b, %Y")


def email_lookup(num):
    with open("num_sheet.json") as data:
        num_dict = json.load(data)
        to_email = {value for (key, value) in num_dict.items() if str(num) == key}
        return to_email.pop()


def send_email(to_email, txt_from, txt_to, txt_body):
    """Send a templated email with SendGrid."""
    mail = Mail()
    mail.from_email = f"{txt_from}@berthfield.com"
    mail.subject = f'SMS from {txt_from} for {txt_to}.'
    mail.to_emails = txt_to
    mail.html_content = f'<p>{txt_body}</p>'

    response = sg.send(mail)
    print(response.status_code, response.body, response.headers)
    # sg.client.mail.send.post(request_body=mail.get())



# HomePage
@app.route('/')
def homepage():
    return render_template("index.html", present_date=formatted_date)


@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Respond to SMS."""
    plat = request.form.get('provider', '')

    if plat.lower() == "twilio":
        sms_from = request.form.get('From', '')
        sms_to = request.form.get('To', '')
        sms_txt = request.form.get('Body', '')

        address = email_lookup(sms_to)
        if address:
            send_email(to_email=address, txt_from=sms_from, txt_body=sms_txt, txt_to=sms_to)

    elif plat.lower() == "anveo":
        sms_from = request.form.get('from', '')
        sms_to = request.form.get('to', '')
        sms_txt = request.form.get('message', '')

        address = email_lookup(sms_to)
        if address:
            send_email(to_email=address, txt_from=sms_from, txt_body=sms_txt, txt_to=sms_to)

    else:
        return (
            "<Response><Message>"
            "Invalid Provider."
            "</Message></Response>"
        )


email = email_lookup(sms_to)
    #

# # Run Server
# if app.__name__ == "__main__":
#     app.run()
