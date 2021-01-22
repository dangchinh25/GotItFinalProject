import importlib
import os

env = os.getenv("FLASK_ENV", "dev")

config = importlib.import_module("main.config." + env).config