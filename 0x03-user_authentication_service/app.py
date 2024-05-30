#!/usr/bin/env python3
""" Setup Basic Flask App"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", strict_slashes=False)
def root():
    """ GET /
    Returns jsonified message """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """ POST /users
    Expects 2 form fields email and password

    Returns:
        200: on success
        400: on failure"""

    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ POST /sessions

    Create a new session for a user
    Expects form fields email and password

    Returns:
        200: on success
        401: on failure
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)

    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=True)
def logout():
    """ DELETE /sessions
    Deletes user session and redirects to /
    otherwise responses with 403 status."""

    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user and session_id:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """ GET /profile
    Returns
        200: on success
        403: on failure """

    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user and session_id:
        return jsonify({"email": user.email})
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
