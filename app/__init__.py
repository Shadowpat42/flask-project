from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "helloworld"

USERS = []  # list for object of type User

from app import views
from app import models
from app import tests
from app import forms
