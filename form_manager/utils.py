"""General helper functions."""
import datetime
import functools
import secrets

import flask
import pymongo
import requests


def prepare_db(db_config: dict) -> tuple:
    """
    Prepare a connection to a mongo database.

    Args:
        db_config (dict): Config for the db
    Returns:
        tuple: (client, db)
    """
    client = get_dbclient(db_config)
    return (client, get_db(client, db_config.get("database")))


def get_dbclient(db_config: dict) -> pymongo.mongo_client.MongoClient:
    """
    Get the connection to the MongoDB database server.

    Args:
        db_config (dict): Database configuration
    Returns:
        pymongo.mongo_client.MongoClient: The client connection.
    """
    return pymongo.MongoClient(
        host=db_config.get("host"),
        port=db_config.get("port"),
        username=db_config.get("username"),
        password=db_config.get("password"),
    )


def get_db(dbclient: pymongo.mongo_client.MongoClient, db_name) -> pymongo.database.Database:
    """
    Get the connection to the MongoDB database.

    Args:
        dbclient (pymongo.mongo_client.MongoClient): Connection to the database.
        db_name: The name of the database

    Returns:
        pymongo.database.Database: The database connection.
    """
    return dbclient.get_database(db_name)


def make_timestamp():
    """
    Generate a timestamp of the current time.

    returns:
        datetime.datetime: The current time.
    """
    return datetime.datetime.now()


def verify_recaptcha(secret: str, response: str):
    """
    Verify the secret from a recaptcha.

    Args:
        secret (str): The secret value for the recaptcha
        response (str): The response value from the form (g-recaptcha-response)

    Returns:
        bool: Whether the check passed
    """
    rec_check = requests.post(
        "https://www.google.com/recaptcha/api/siteverify", {"secret": secret, "response": response}
    )
    return bool(rec_check.json().get("success"))


def login_required(func):
    """Check whether user is logged in, ottherwise return 403."""
    @functools.wraps(func)
    def inner(*args, **kwargs):
        if not flask.session.get("email"):
            flask.abort(status=403)
        return func(*args, **kwargs)
    return inner


def generate_id():
    """Generate an identifier for a form entry."""
    return secrets.token_urlsafe(12)
