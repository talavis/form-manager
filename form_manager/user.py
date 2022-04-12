"""Endpoints related to auth."""
import flask


blueprint = flask.Blueprint("user", __name__)  # pylint: disable=invalid-name


@blueprint.route("/login")
def oidc_login():
    """Perform a login using OpenID Connect."""
    redirect_uri = flask.url_for("user.oidc_authorize", _external=True)
    return oauth.oidc_entry.authorize_redirect(redirect_uri)


@blueprint.route("/login/authorize")
def oidc_authorize():
    """Authorize a login using OpenID Connect (e.g. Elixir AAI)."""
    token = oauth.oidc_entry.authorize_access_token()
    flask.session["email"] = token.get(["userinfo"], {}).get("email")
    flask.session.permanent = True
    return flask.redirect("/")


@blueprint.route("/logout", methods=["POST"])
def logout():
    flask.session.clear()
    flask.session.permanent = False
