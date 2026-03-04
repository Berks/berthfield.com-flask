# import Flask App
from flask import Flask,render_template
import os
import logging.config
import dicts
from handlers import routes

# Imports for Security
from flask_talisman import Talisman

# Import Google Cloud Logging
try:
    import google.cloud.logging
    client = google.cloud.logging.Client()
    client.setup_logging()
    logging.config.dictConfig(dicts.LOG_CONFIG)
except ImportError:
    # Fallback for local development if GCP libs aren't installed
    import logging
    logging.basicConfig(level=logging.INFO)

# Imports for Security
from flask_talisman import Talisman

app = Flask(__name__)

# Wrap with taliban for security
talisman = Talisman(
    app,
    content_security_policy=dicts.csp,
    force_https=False
)

# URLS
app.add_url_rule(rule="/", endpoint="index.html", view_func=routes.homepage, methods=["GET"])
app.add_url_rule(rule="/methods-twil", endpoint="methods-twil", view_func=routes.incoming_twil_sms, methods=["GET", "POST"])
app.add_url_rule(rule="/methods-anv", endpoint="methods-anv", view_func=routes.incoming_anv_sms, methods=["GET", "POST"])



if __name__ == '__main__':
    if not os.getenv('GAE_ENV', '').startswith('standard'):
        app.run(port=8000, host="localhost", debug=True)  # localhost
    else:
        app.run()  # production


