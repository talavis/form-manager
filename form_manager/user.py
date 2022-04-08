"""Endpoints related to auth."""
import flask


blueprint = flask.Blueprint("user", __name__)  # pylint: disable=invalid-name


@blueprint.route("/login", methods=["POST"])
def login():
    form_response = dict(flask.request.json)
    flask.session["email"] = form_response.get("email")
    return flask.Response(status="200")


@blueprint.route("/logout", methods=["POST"])
def logout():
    flask.session.clear()
