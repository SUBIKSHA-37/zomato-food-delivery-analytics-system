"""
config.py - Configuration settings for Flask app
"""

import os

class Config:
    # ── Security ──────────────────────────────────────────
    SECRET_KEY = os.environ.get("SECRET_KEY", "zomato-secret-key-change-in-production")

    # ── MySQL Database ────────────────────────────────────
    MYSQL_HOST     = os.environ.get("MYSQL_HOST",     "localhost")
    MYSQL_PORT     = int(os.environ.get("MYSQL_PORT", 3306))
    MYSQL_USER     = os.environ.get("MYSQL_USER",     "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "yourpassword")
    MYSQL_DB       = os.environ.get("MYSQL_DB",       "zomatoapp")

    # SQLAlchemy connection string
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── App Settings ──────────────────────────────────────
    DEBUG = os.environ.get("FLASK_DEBUG", "True") == "True"
    TESTING = False
    JSON_SORT_KEYS = False   # Keep JSON key order