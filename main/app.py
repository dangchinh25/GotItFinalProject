import logging

from flask import Flask, jsonify

from main.db import db
from main.config import config
from main.exceptions import BaseError

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"message": str(error), "error": {}}), 404


@app.errorhandler(BaseError)
def handle_customized_error(error):
    return jsonify({"message": error.message, "error": error.error}), error.status_code


@app.errorhandler(Exception)
def handle_general_error(error):
    logging.exception(error)
    return jsonify({"message": "Internal server error", "error": {}})


