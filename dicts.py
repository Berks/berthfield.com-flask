# Configuration structure for GCP Logging
OG_CONFIG = {
    "version": 1,
    "formatters": {
        "json": {
            "()": "flask_google_cloud_logger.FlaskGoogleCloudFormatter",
            "application_info": {
                "type": "python-application",
                "application_name": "Antonio-Portfolio"
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
        "root": {"level": "INFO", "handlers": ["json"]},
        "werkzeug": {"level": "WARN", "handlers": ["json"]}
    }
}

#   Content security Policy
#   Allows scripts and offsite-content to be displayed.
#   Defaults to blocking all and allowing from the whitelist below

csp = {
    'default-src': [
        '\'self\'',
        'fonts.googleapis.com',
        'fonts.gstatic.com',
        'cdnjs.cloudflare.com',
    ],
    'style-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'fonts.googleapis.com',
        'cdnjs.cloudflare.com'
    ],
    'font-src': [
        '\'self\'',
        'fonts.gstatic.com',
        'cdnjs.cloudflare.com'
    ],
    'img-src': [
        '\'self\'',
        'data:',
        'www.codewars.com'
    ],
    'script-src': [
        '\'self\'',
        'cdnjs.cloudflare.com'
    ]
}
