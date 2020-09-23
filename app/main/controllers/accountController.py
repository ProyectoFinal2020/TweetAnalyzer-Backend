import hashlib
import urllib
import os
import flask
from flask import redirect, url_for, request
from .. import firebase
from ..auth.auth import save_user
from ..serializers.authDto import AuthDto
from flask_login import login_required, logout_user, current_user
from flask_restx import Resource

api = AuthDto.api
user = AuthDto.user
firebaseUser = AuthDto.firebaseUser

auth = firebase.auth()


@api.route('/verifyIdToken/<string:idToken>')
class verifyIdToken(Resource):
    @api.marshal_with(user)
    def get(self, idToken):
        """
        Logs the user in with Firebase email login
        """
        try:
            user = auth.get_account_info(idToken)
            user_id = int(hashlib.sha256(user["users"][0]["localId"].encode(
                'utf-8')).hexdigest(), 16) % 10 ** 256
            save_user(
                provider="firebase",
                user_id=user_id,
                token={"token": idToken},
                username=user["users"][0]["email"],
                photo_url="",
                emailVerified=user["users"][0]["emailVerified"]
            )
            return current_user
        except:
            pass
        return None

    @api.expect(firebaseUser)
    @api.marshal_with(user)
    def post(self, idToken):
        """
        Registers the user in with Firebase email login
        """
        try:
            firebaseUser = request.json
            user = auth.get_account_info(idToken)
            user_id = int(hashlib.sha256(user["users"][0]["localId"].encode(
                'utf-8')).hexdigest(), 16) % 10 ** 256
            save_user(
                provider="firebase",
                user_id=user_id,
                token={"token": idToken},
                username=firebaseUser["name"],
                photo_url=firebaseUser["photoUrl"],
                emailVerified=user["users"][0]["emailVerified"]
            )
            return current_user
        except:
            pass
        return None


@api.route('/login/twitter')
class twitter_login(Resource):
    @api.doc(params={'url': 'Callback URL'})
    def get(self):
        """
        Logs the user in with Twitter login
        """
        if not current_user.is_authenticated:
            url = request.args.get(
                'url', os.getenv('URL', settings.URL), type=str)
            url = urllib.parse.unquote(url)
            flask.session["next_url"] = url
            return redirect(url_for("twitter.login"))
        else:
            return "Ya existe un usuario autenticado: {}".format(current_user.name)


@api.route('/login/github')
class github_login(Resource):
    @api.doc(params={'url': 'Callback URL'})
    def get(self):
        """
        Logs the user in with Github login
        """
        if not current_user.is_authenticated:
            url = request.args.get(
                'url', os.getenv('URL', settings.URL), type=str)
            url = urllib.parse.unquote(url)
            flask.session["next_url"] = url
            return redirect(url_for("github.login"))
        else:
            return "Ya existe un usuario autenticado: {}".format(current_user.name)


@api.route('/login/google')
class google_login(Resource):
    @api.doc(params={'url': 'Callback URL'})
    def get(self):
        """
        Logs the user in with Google login
        """
        if not current_user.is_authenticated:
            url = request.args.get(
                'url', os.getenv('URL', settings.URL), type=str)
            url = urllib.parse.unquote(url)
            flask.session["next_url"] = url
            return redirect(url_for("google.login"))
        else:
            return "Ya existe un usuario autenticado: {}".format(current_user.name)


@api.route('/login/facebook')
class facebook_login(Resource):
    @api.doc(params={'url': 'Callback URL'})
    def get(self):
        """
        Logs the user in with Facebook login
        """
        if not current_user.is_authenticated:
            url = request.args.get(
                'url', os.getenv('URL', settings.URL), type=str)
            url = urllib.parse.unquote(url)
            flask.session["next_url"] = url
            return redirect(url_for("facebook.login"))
        else:
            return "Ya existe un usuario autenticado: {}".format(current_user.name)


@api.route('/isAuthenticated')
class IsAuthenticated(Resource):
    def get(self):
        """
        Returns whether the user is authenticated or not
        """
        return current_user.is_authenticated


@api.route('/userInformation')
class UserInformation(Resource):
    @login_required
    @api.marshal_with(user)
    def get(self):
        """
        Returns additional user information if there is a user logged in
        """
        return current_user


@api.route('/logout')
class Logout(Resource):
    @login_required
    def get(self):
        """
        Logs the current user out
        """
        logout_user()
        return "You are logged out."
