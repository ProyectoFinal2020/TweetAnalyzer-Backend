from flask_restx import Namespace, fields


class AuthDto:
    api = Namespace('account', description='Operations related to users')
    user = api.model('User', {
        'id': fields.Integer(required=True, description="Id of the existing user"),
        'name': fields.String(required=True, description="Name of the existing user"),
        'photoUrl': fields.String(description="Profile picture of the existing user"),
        'emailVerified': fields.Boolean(description="Returns true if the user has verified his/her email")
    })
    firebaseUser = api.model('FirebaseUser', {
        'name': fields.String(required=True, description="Id of the existing user"),
        'photoUrl': fields.String(description="Profile picture of the existing user")
    })
