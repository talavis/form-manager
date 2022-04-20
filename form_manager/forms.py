"""Endpoints related to forms."""
import flask
import flask_mail

from . import mail
from . import utils

blueprint = flask.Blueprint("forms", __name__)  # pylint: disable=invalid-name

def form():
    """The data structure for a form"""
    return {
        "identifier": utils.generate_id(),
        "title": "",
        "recaptcha_secret": "",
        "email_recipients": [],
        "owner": "",
        "redirect": "",
    }


def validate_form(indata: dict, reference: dict) -> bool:
    """
    Validate that the incoming data matches the form data structure.

    * No extra properties
    * All indata is of the correct type
    * Identifier is not modified

    Args:
        indata (dict): The data to be validated.
        reference (dict): The data structure to use as reference (entry or form()).

    Returns:
        bool: Whether the validation passed or not.
    """
    for prop in indata:
        if prop not in reference:
            flask.current_app.logger.debug("Extra property")
            return False
        if not type(indata[prop]) == type(reference[prop]):
            flask.current_app.logger.debug("Wrong property type")
            return False
    for prop in ("identifier", "owner"):
        if prop in indata:
            if indata[prop] != reference[prop]:
                flask.current_app.logger.debug("Trying to set %s", prop)
                return False
    return True


@blueprint.route("", methods=["GET"])
@utils.login_required
def list_forms():
    """List all forms belonging to the current user."""
    form_info = list(flask.g.db["forms"].find({"owner": flask.session.get("email")}, {"_id": 0}))
    return flask.jsonify(
        {"forms": form_info, "url": flask.url_for("forms.list_forms", _external=True)}
    )


@blueprint.route("/<identifier>", methods=["GET"])
@utils.login_required
def get_form_info(identifier: str):
    """
    Get information about a form.

    Args:
        identifier (str): The form identifier.
    """
    entry = flask.g.db["forms"].find_one({"identifier": identifier})
    if not entry:
        flask.abort(status=404)
    if flask.session["email"] != entry["owner"]:
        flask.abort(status=403)
    return flask.jsonify(
        {"form": entry, "url": flask.url_for("forms.get_form_info", _external=True)}
    )


@blueprint.route("", methods=["POST"])
@utils.login_required
def add_form():
    """Add a new form for the current user."""
    indata = flask.request.get_json(silent=True)
    if not indata:
        indata = {}
    entry = form()
    while flask.g.db["forms"].find_one({"identifier": entry["identifier"]}):
        entry["identifier"] = utils.generate_id()
    if not validate_form(indata, entry):
        flask.current_app.logger.debug("Validation failed")
        flask.abort(status=400)
    entry.update(indata)
    entry["owner"] = flask.session["email"]
    flask.g.db["forms"].insert_one(entry)
    return flask.jsonify({"identifier": entry["identifier"], "url": flask.url_for("forms.add_form", _external=True)})


@blueprint.route("/<identifier>", methods=["PATCH"])
@utils.login_required
def edit_form(identifier: str):
    """
    Edit a form for the current user.

    Args:
        identifier (str): The form identifier.
    """
    indata = flask.request.json
    entry = flask.g.db["forms"].find_one({"identifier": identifier})
    if not entry:
        flask.abort(status=404)
    if flask.session["email"] != entry["owner"]:
        flask.abort(status=403)
    if not validate_form(indata, entry):
        flask.current_app.logger.debug("Validation failed")
        flask.abort(status=400)
    entry.update(indata)
    flask.g.db["forms"].update_one({"_id": entry["_id"]}, {"$set": entry})
    return flask.Response(status=200)


@blueprint.route("/<identifier>", methods=["DELETE"])
@utils.login_required
def delete_form(identifier: str):
    """
    Delete a form for the current user.

    Args:
        identifier (str): The form identifier.
    """
    entry = flask.g.db["forms"].find_one({"identifier": identifier})
    if not entry:
        flask.abort(status=404)
    if flask.session["email"] != entry["owner"]:
        flask.abort(status=403)
    flask.g.db["forms"].delete_one(entry)
    flask.g.db["responses"].delete_many({"identifier": entry[identifier]})
    return flask.Response(status=200)


@blueprint.route("/<identifier>/incoming", methods=["POST"])
def receive_response(identifier: str):
    """
    Save a form response to the db.

    Args:
        identifier (str): The form identifier.
    """
    form_info = flask.g.db["forms"].find_one({"identifier": identifier})
    if not form_info:
        return flask.abort(status=400)
    form_response = dict(flask.request.form)

    if form_info.get("recaptcha_secret"):
        if not utils.verify_recaptcha(
            form_info.get("recaptcha_secret"), form_response.get("g-recaptcha-response")
        ):
            flask.abort(status=400)

    if form_info.get("email_recipients"):
        mail.send(
            flask_mail.Message(
                f"Form from {form_info.get('title')}",
                body=form_response,
                recipients=form_info["email_recipients"],
            )
        )

    to_add = {
        "response": form_response,
        "timestamp": utils.make_timestamp(),
        "identifier": identifier,
    }

    flask.g.db[f"responses"].insert_one(to_add)

    return flask.Response(status=200)


@blueprint.route("/<identifier>/responses", methods=["GET"])
@utils.login_required
def get_responses(identifier):
    """
    List form responses.

    Args:
        identifier (str): The form identifier.
    """

    form_info = flask.g.db["forms"].find_one({"identifier": identifier})
    if flask.session["email"] != form_info["owner"]:
        flask.abort(status=403)
    responses = list(flask.g.db["responses"].find({"identifier": identifier}, {"_id": 0}))
    return flask.jsonify(
        {
            "responses": responses,
            "url": flask.url_for("forms.get_responses", identifier=identifier, _external=True),
        }
    )
