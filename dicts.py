# Configuration structure for GCP Logging
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