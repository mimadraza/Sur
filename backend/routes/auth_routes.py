from flask import Blueprint, request, jsonify
from services import login_user

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    response = login_user(data.get('email'), data.get('password'))
    return jsonify(response)