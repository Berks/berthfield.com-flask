# import Flask App
from flask import Flask
import os

# Imports for logging
from flask import request, g
import logging
from logging import config
from flask_google_cloud_logger import FlaskGoogleCloudLogger

# Imports for Security
from flask_talisman import Talisman

from handlers import routes
import dicts

app = Flask(__name__)

# URLS
app.add_url_rule(rule="/", endpoint="index.html", view_func=routes.homepage, methods=["GET"])
app.add_url_rule(rule="/blog", endpoint="blog", view_func=routes.blog, methods=["GET"])
app.add_url_rule(rule="/blog/post.html", endpoint="/blog/post.html", view_func=routes.post, methods=["GET", "POST"])
app.add_url_rule(rule="/methods-twil", endpoint="methods-twil", view_func=routes.incoming_twil_sms, methods=["GET", "POST"])
app.add_url_rule(rule="/methods-anv", endpoint="methods-anv", view_func=routes.incoming_anv_sms, methods=["GET", "POST"])


# Incorporate Logging
config.dictConfig(dicts.LOG_CONFIG)  # load log config from dict
logger = logging.getLogger("root")  # get root logger instance

FlaskGoogleCloudLogger(app)


@app.teardown_request  # log request and response info after extension's callbacks
def log_request_time(_exception):
    logger.info(
        f"{request.method} {request.path} - Sent {g.response.status_code}" +
        " in {g.request_time:.5f}ms")

# Wrap with taliban for security
Talisman(app, content_security_policy=dicts.csp)

if __name__ == '__main__':
    if os.getenv('GAE_ENV', '').startswith('standard'):
        app.run()  # production
    else:
        app.run(port=8000, host="localhost", debug=True)  # localhost


