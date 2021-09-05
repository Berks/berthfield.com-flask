from flask import Flask
from flask import request, g
from flask_talisman import Talisman

# import logging
import logging
from logging import config
from flask_google_cloud_logger import FlaskGoogleCloudLogger

app = Flask(__name__)


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

config.dictConfig(LOG_CONFIG)  # load log config from dict
logger = logging.getLogger("root")  # get root logger instance

FlaskGoogleCloudLogger(app)


@app.teardown_request  # log request and response info after extension's callbacks
def log_request_time(_exception):
    logger.info(
        f"{request.method} {request.path} - Sent {g.response.status_code}" +
        " in {g.request_time:.5f}ms")

#   Content security Policy
#   Allows scripts and offsite-content to be displayed.
#   Defaults to blocking all and allowing from the whitelist below
csp = {
    'default-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        # Google Fonts
        'fonts.googleapis.com',
        'fonts.gstatic.com',
        # Bootstrap
        'stackpath.bootstrapcdn.com',
        # Jquery
        'code.jquery.com',
        'cdn.jsdelivr.net',
        # Others
        '*.fontawesome.com',
        'www.codewars.com',

        ],
}


Talisman(app, content_security_policy=csp)

from app import routes
