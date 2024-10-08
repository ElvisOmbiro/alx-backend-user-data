#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
import json


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


auth = None
AUTH_TYPE = getenv("AUTH_TYPE")

if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif AUTH_TYPE == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif AUTH_TYPE == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif AUTH_TYPE == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()


@app.before_request
def before_request():
    """
    Before request
    """
    if auth is None:
        return

    allowed_paths = [
        "/api/v1/status/",
        "/api/v1/unauthorized/",
        "/api/v1/forbidden/",
        "/api/v1/auth_session/login/",
    ]

    if not auth.require_auth(request.path, allowed_paths):
        return

    if auth.authorization_header(request) is None \
            and auth.session_cookie(request) is None:
        abort(401)

    current_user = auth.current_user(request)

    if current_user is None:
        abort(403)

    request.current_user = current_user


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Not found error handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """
    Unauthorized error handler
    """
    response_data = {"error": "Unauthorized"}

    return jsonify(response_data), 401


@app.errorhandler(403)
def forbidden_error(error) -> str:
    """
    Forbidden error handler

