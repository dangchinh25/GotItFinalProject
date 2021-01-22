from main.db import db
from main.app import app

with app.app_context():
    db.create_all()