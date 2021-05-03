from flask import Flask, render_template, request
import os
import datetime

# Imports for the twilio sms endpoint
import sendgrid
from sendgrid.helpers.mail import Email, Mail, Personalization
from validate_email import validate_email

# Create sendgrid instance
sg = sendgrid.SendGridAPIClient(api_key=os.environ["SENDGRID_API_KEY"])
# Create flask instance
app = Flask(__name__)

# Set attribute to mitigate error in dev environ... Not sure of the root cause
app.__name__ = "__main__"
# app.name = "Berthfield Server"

# Get formatted date for the index template.
date = datetime.datetime.now()
formatted_date = date.strftime("%b, %Y")


def send_email(to_email):
    """Send a templated email with SendGrid."""
    personalization = Personalization()
    personalization.add_to(Email(to_email))
    mail = Mail()
    mail.add_personalization(personalization)
    mail.from_email = Email("owl@example.com")
    mail.subject = "Ahoy from Twilio + SendGrid!"
    mail.template_id = os.environ["TEMPLATE_ID"]
    sg.client.mail.send.post(request_body=mail.get())


# HomePage
@app.route('/')
def homepage():
    return render_template("index.html", present_date=formatted_date)


@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Respond to SMS."""
    email = request.form.get('Body', None)

    if email is None or not validate_email(email):
        return (
            "<Response><Message>"
            "Please provide a valid email address."
            "</Message></Response>"
        )

    send_email(email)
    return "<Response><Message>Coding is fun!</Message></Response>"


# Run Server
# if app.__name__ == "__main__":
#     app.run()
