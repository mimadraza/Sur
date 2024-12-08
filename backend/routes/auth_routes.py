from flask import Blueprint, request, jsonify
from services.auth_services import login_user
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    response = login_user(data.get('email'), data.get('password'))
    return jsonify(response)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    response = register(data.get('firstName'), data.get('lastName'), data.get('dateOfBirth'), data.get('country'),data.get('email'), data.get('password'))
    return jsonify(response)

@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    # Clear the token cookie
    response = logout()
    return response