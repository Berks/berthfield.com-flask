from flask import Flask

app = Flask(__name__)
app.__name__ = "__main__"

from app import routes
