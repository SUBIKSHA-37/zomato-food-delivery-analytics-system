"""
db.py - Database connection module
Uses PyMySQL for direct queries (simple and beginner-friendly)
"""

import pymysql
from flask import g, current_app


def get_db():
    """
    Get database connection.
    Stores connection in Flask's 'g' object so it's reused
    within the same request.
    """
    if "db" not in g:
        g.db = pymysql.connect(
            host=current_app.config["MYSQL_HOST"],
            port=current_app.config["MYSQL_PORT"],
            user=current_app.config["MYSQL_USER"],
            password=current_app.config["MYSQL_PASSWORD"],
            database=current_app.config["MYSQL_DB"],
            cursorclass=pymysql.cursors.DictCursor,   # Returns rows as dicts
            autocommit=False,
        )
    return g.db


def close_db(e=None):
    """Close database connection at end of request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db_teardown(app):
    """Register db teardown with the app."""
    app.teardown_appcontext(close_db)


def query(sql, params=None, fetch_one=False, commit=False):
    """
    Helper function to run SQL queries easily.

    Args:
        sql      : SQL string with %s placeholders
        params   : tuple of values to bind
        fetch_one: True → return one row dict, False → return list
        commit   : True → commit (for INSERT/UPDATE/DELETE)

    Returns:
        dict | list | lastrowid (int for INSERT)
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(sql, params or ())

    if commit:
        db.commit()
        return cursor.lastrowid    # Useful for INSERT statements
    elif fetch_one:
        return cursor.fetchone()   # Returns dict or None
    else:
        return cursor.fetchall()   # Returns list of dicts