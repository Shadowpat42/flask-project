from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "helloworld"

USERS = []

from app import views, tests, forms
