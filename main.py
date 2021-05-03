from flask import Flask, render_template, request
import os
import datetime
import json

# Imports for the twilio sms endpoint
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
# from validate_email import validate_email

# Create sendgrid instance
sg = SendGridAPIClient(api_key=os.environ["SENDGRID_API_KEY"])

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
    mail = Mail(
        from_email = f"{txt_from}@berthfield.com",
        to_emails = f"{to_email}",
        subject = f'SMS from {txt_from} for {txt_to}.',
        html_content = f'{txt_to}'
    )

    try:
        response = sg.send(mail)
        # print(response)
        print(response.status_code, response.body, response.headers)
    except Exception as e:
        print(e.message)
    #sg.client.mail.send.post(request_body=mail.get())
    #print(f"from email: {mail.from_email}")
    #print(f"To: {mail.to_emails}")
    #print(f"body: {mail.html_content}")


# HomePage
@app.route('/')
def homepage():
    return render_template("index.html", present_date=formatted_date)


@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Respond to SMS."""
    plat = request.args['provider']

    print(plat)

    if plat == 'twilio':
        sms_from = request.args['From']
        sms_to = request.args['To']
        sms_txt = request.args['Body']

        address = email_lookup(sms_to)
        if address:
            send_email(to_email=address, txt_from=sms_from, txt_body=sms_txt, txt_to=sms_to)

    elif plat == 'anveo':
        sms_from = request.args['from']
        sms_to = request.args['to']
        sms_txt = request.args['message']

        address = email_lookup(sms_to)
        if address:
            send_email(to_email=address, txt_from=sms_from, txt_body=sms_txt, txt_to=sms_to)

    else:
        return (
            "<Response><Message>"
            f"Invalid Provider.{plat}"
            "</Message></Response>"
        )


# email = email_lookup(sms_to)
    #

# # Run Server
# if app.__name__ == "__main__":
#     app.run(debug=True)
