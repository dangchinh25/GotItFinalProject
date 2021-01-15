from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from main.db import db
from main.config import config
from main.exceptions import BaseError

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


# Register error handler for our Flask app
@app.errorhandler(BaseError)
def handle_customized_error(error):
    return jsonify({"message": error.message, "error": error.error_data}), error.status_code