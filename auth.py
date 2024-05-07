# auth.py

from flask import request, jsonify
from flask_login import login_user, logout_user, login_required
from models import User  # Assuming you have a User model defined

def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({"message": "Logged in successfully"})
    return jsonify({"message": "Invalid credentials"}), 401

@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"})
