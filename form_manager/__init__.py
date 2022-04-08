"""Initialize Flask app."""

import logging

import flask
import flask_mail
from werkzeug.middleware.proxy_fix import ProxyFix

from form_manager import config, forms, user, utils

mail = flask_mail.Mail()


def create_app():
    """Construct the core application."""
    app = flask.Flask(__name__, instance_relative_config=False)
    app.config.from_object("form_manager.config.Config")
    app.config.from_envvar("CONFIG_FILE", silent=True)

    @app.before_request
    def prepare():
        """Set up the database connection"""
        flask.g.dbclient, flask.g.db = utils.prepare_db(flask.current_app.config["DB_CONF"])

    @app.after_request
    def finalize(response):
        """Finalize the response and clean up."""
        # close db connection
        if hasattr(flask.g, "dbclient"):
            flask.g.dbclient.close()
            # add some headers for protection
            response.headers["X-Frame-Options"] = "SAMEORIGIN"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            return response

    if __name__ != "__main__":
        gunicorn_logger = logging.getLogger("gunicorn.error")
        if gunicorn_logger:
            app.logger.handlers = gunicorn_logger.handlers
            app.logger.setLevel(gunicorn_logger.level)

    mail.init_app(app)
    app.extensions["mail"].debug = 0

    if app.config["REVERSE_PROXY"]:
        app.wsgi_app = ProxyFix(app.wsgi_app)

    app.register_blueprint(forms.blueprint, url_prefix="/api/v1/form")
    app.register_blueprint(user.blueprint, url_prefix="/api/v1/user")
        
    @app.route("/api/v1/heartbeat/", methods=["GET"])
    def heartbeat():
        return flask.Response(status=200)

    return app
