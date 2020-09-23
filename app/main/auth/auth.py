import flask
from flask import flash

from ..entities import db
from ..entities.user import OAuth, User
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_login import current_user, login_user
from sqlalchemy.orm.exc import NoResultFound
from . import twitter_blueprint, google_blueprint, facebook_blueprint, github_blueprint


def save_user(provider, user_id, token, username, photo_url, emailVerified):
    user_id = str(user_id)
    query = OAuth.query.filter_by(provider=provider, provider_user_id=user_id)
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(provider=provider,
                      provider_user_id=user_id, token=token)

    if oauth.user:
        oauth.user.emailVerified = emailVerified
        db.session.commit()
        login_user(oauth.user)
    else:
        user = User(name=username, photoUrl=photo_url,
                    emailVerified=emailVerified)
        oauth.user = user
        db.session.add_all([user, oauth])
        db.session.commit()
        login_user(user)


def find_or_save_user(blueprint, session_get, attribute_name, token):
    if not token:
        flash("Failed to log in.", category="error")
        return False

    resp = blueprint.session.get(session_get)
    if not resp.ok:
        msg = "Failed to fetch user info."
        flash(msg, category="error")
        return False

    info = resp.json()
    user_id = info[attribute_name["id"]]
    username = info[attribute_name["username"]]
    photo_url = info[attribute_name["photoUrl"]]
    if blueprint.name == "facebook":
        photo_url = photo_url["data"]["url"]

    save_user(blueprint.name, user_id, token, username, photo_url, True)

    next_url = flask.session["next_url"]
    redir = flask.redirect(next_url)
    redir.headers['headers'] = token
    return redir


def show_error(blueprint, message, response):
    msg = "OAuth error from {name}! " "message={message} response={response}".format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")


@oauth_authorized.connect_via(twitter_blueprint)
def twitter_logged_in(blueprint, token):
    return find_or_save_user(
        blueprint=blueprint,
        session_get='account/verify_credentials.json',
        attribute_name={"id": "id", "username": "screen_name",
                        "photoUrl": "profile_image_url"},
        token=token
    )


@oauth_error.connect_via(twitter_blueprint)
def twitter_error(blueprint, message, response):
    show_error(blueprint, message, response)


@oauth_authorized.connect_via(github_blueprint)
def github_logged_in(blueprint, token):
    return find_or_save_user(
        blueprint=blueprint,
        session_get='/user',
        attribute_name={"id": "id", "username": "login",
                        "photoUrl": "avatar_url"},
        token=token
    )


@oauth_error.connect_via(github_blueprint)
def github_error(blueprint, message, response):
    show_error(blueprint, message, response)


@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    return find_or_save_user(
        blueprint=blueprint,
        session_get='/oauth2/v1/userinfo?alt=json',
        attribute_name={"id": "id", "username": "name", "photoUrl": "picture"},
        token=token
    )


@oauth_error.connect_via(google_blueprint)
def google_error(blueprint, message, response):
    show_error(blueprint, message, response)


@oauth_authorized.connect_via(facebook_blueprint)
def facebook_logged_in(blueprint, token):
    return find_or_save_user(
        blueprint=blueprint,
        session_get='/me?fields=id,name,picture',
        attribute_name={"id": "id", "username": "name", "photoUrl": "picture"},
        token=token
    )


@oauth_error.connect_via(facebook_blueprint)
def facebook_error(blueprint, message, response):
    show_error(blueprint, message, response)
