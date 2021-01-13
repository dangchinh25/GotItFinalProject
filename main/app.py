from flask import Flask

from main.db import db
from main.config import config

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)