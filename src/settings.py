import os

DATABASE_URL = os.environ["DATABASE_URL"]
DEBUG = os.environ.get("DEBUG") == "1"
