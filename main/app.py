from flask import Flask, jsonify

from main.db import db
from main.config import config
from main.exceptions import BaseError

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(404)
def page_not_found(error):
    app.logger.info(str(error))
    return jsonify({"message": str(error), "error": {}}), 404


@app.errorhandler(BaseError)
def handle_customized_error(error):
    return jsonify({"message": error.message, "error": error.error}), error.status_code

