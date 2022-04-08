"""Endpoints related to forms."""
import flask

from form_manager import utils

blueprint = flask.Blueprint("forms", __name__)  # pylint: disable=invalid-name


@blueprint.route("/<form_identifier>", methods=["POST"])
def suggest_form(form_identifier:str):
    """
    Save the response for the form to the db.

    Args:
        form_identifier (str): The identifier for the submitted form
    """
    form_info = flask.g.db["forms"].find_one({"identifier": form_identifier})
    if not form_info:
        return flask.abort(status=400)
    form_response = dict(flask.request.form)

    to_add = {
        "response": form_response,
        "timestamp": utils.make_timestamp()
    }
    
    flask.g.db[f"form_{form_identifier}"].insert_one(to_add)

    if form_info.get("target_email"):
        utils.send_email()
    return flask.Response(page, status=200)


@blueprint.route("/<entry>/list/", methods=["GET"])
def get_entry_list(entry):
    args = dict(flask.request.args)
    token = args.get("token")
    if not token or token not in flask.current_app.config.get("getToken"):
        return flask.Response(status=401)
    if entry == "add_biobank":
        hits = list(flask.g.db["responsesAddBiobank"].find({}, {"_id": 0}))
    elif entry == "add_collection":
        hits = list(flask.g.db["responsesAddCollection"].find({}, {"_id": 0}))
    elif entry == "suggestion":
        hits = list(flask.g.db["suggestions"].find({}, {"_id": 0}))
    else:
        return flask.Response(status=404)
    return flask.jsonify(hits)
