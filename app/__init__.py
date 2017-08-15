import requests
import json
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

jtiToken = "No Token"

from app import views
