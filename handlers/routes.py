from methods import sms
from flask import render_template, request
import datetime


# Get formatted date for the index template.
date = datetime.datetime.now()
formatted_date = date.strftime("%b, %Y")


# Defines routes for the Flask Application
def homepage():
    return render_template("index.html", present_date=formatted_date)


def blog():
    return render_template("blog.html")


def post():
    return render_template("post.html")


def incoming_twil_sms():
    """Parses the incoming request and calls the send email function."""
    sms_from = request.form['From']
    print(f"from: {sms_from} type: {type(sms_from)}")
    sms_to = request.form['To']
    sms_txt = request.form['Body']
    address = sms.email_lookup(sms_to)  # Twilio numbers send a +

    if address:
        return str(sms.send_email(to_email=address, txt_from=sms_from, txt_body=sms_txt, txt_to=sms_to))
    else:
        return "invalid number"


def incoming_anv_sms():
    """Parses the incoming request and calls the send email function."""
    sms_from = request.args.get('from', '')
    sms_to = request.args.get('to', '')
    sms_txt = request.args.get('message', '')
    address = sms.email_lookup(sms_to)  # Anveo numbers do not send the +

    if address:
        return str(sms.send_email(to_email=address, txt_from=sms_from, txt_body=sms_txt, txt_to=sms_to))
    else:
        return "invalid number"
