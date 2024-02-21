import os

API_KEY = os.environ["API_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]
DEBUG = os.environ.get("DEBUG") == "1"
