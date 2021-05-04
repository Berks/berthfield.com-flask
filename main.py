from flask import Flask, render_template, request, g
import os
import datetime
import json

# import flask logging
import logging
from logging import config
from flask_google_cloud_logger import FlaskGoogleCloudLogger


# Imports for the twilio sms endpoint
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "json": {
            "()": "flask_google_cloud_logger.FlaskGoogleCloudFormatter",
            "application_info": {
                "type": "python-application",
                "application_name": "Example Application"
            },
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        }
    },
    "handlers": {
        "json": {
            "class": "logging.StreamHandler",
            "formatter": "json"
        }
    },
    "loggers": {
        "root": {
            "level": "INFO",
            "handlers": ["json"]
        },
        "werkzeug": {
            "level": "WARN",  # Disable werkzeug hardcoded logger
            "handlers": ["json"]
        }
    }
}

# Create sendgrid instance
sg = SendGridAPIClient(api_key=os.environ["SENDGRID_API_KEY"])

# Create flask instance
app = Flask(__name__)

config.dictConfig(LOG_CONFIG)  # load log config from dict
logger = logging.getLogger("root")  # get root logger instance
FlaskGoogleCloudLogger(app)


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
        try:
            return to_email.pop()
        except KeyError:
            return False


def send_email(to_email, txt_from, txt_to, txt_body):
    """Send a templated email with SendGrid."""
    mail = Mail(
        from_email=f"{txt_from}@berthfield.com",
        to_emails=f"{to_email}",
        subject=f'SMS from {txt_from} for {txt_to}.',
        html_content=f'{txt_body}'
    )

    try:
        response = sg.send(mail)
        # print(response)
        print(response.status_code, response.body, response.headers)
        return response.status_code
    except Exception as e:
        print(e.message)


# HomePage
@app.route('/')
def homepage():
    return render_template("index.html", present_date=formatted_date)


@app.route("/sms-twil", methods=['GET', 'POST'])
def incoming_twil_sms():
    """Respond to SMS."""
    sms_from = request.form['From']
    print(f"from: {sms_from} type: {type(sms_from)}")
    sms_to = request.form['To']
    sms_txt = request.form['Body']
    address = email_lookup(sms_to)  # Twilio numbers send a +

    if address:
        return str(send_email(to_email=address, txt_from=sms_from, txt_body=sms_txt, txt_to=sms_to))
    else:
        return "invalid number"


@app.route("/sms-anv", methods=['GET', 'POST'])
def incoming_anv_sms():
    """Respond to SMS."""
    sms_from = request.args.get('from', '')
    sms_to = request.args.get('to', '')
    sms_txt = request.args.get('message', '')
    address = email_lookup(sms_to)  # Anveo numbers do not send the +

    if address:
        return str(send_email(to_email=address, txt_from=sms_from, txt_body=sms_txt, txt_to=sms_to))
    else:
        return "invalid number"


@app.teardown_request  # log request and response info after extension's callbacks
def log_request_time(_exception):
    logger.info(
        f"{request.method} {request.path} - Sent {g.response.status_code}" +
        " in {g.request_time:.5f}ms")


# Enable Debug
# app.debug = True


# Run Server
# if app.__name__ == "__main__":
#     app.run(debug=True)
