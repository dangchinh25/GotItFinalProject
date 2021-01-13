import importlib
import os

env = os.getenv("ENV", "dev")

config = importlib.import_module("main.config." + env).config