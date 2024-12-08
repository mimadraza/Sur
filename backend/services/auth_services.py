from flask import make_response, jsonify
from db.queries import get_user_by_email, call_procedure
from utils.hashing import hash_password, check_password
from utils.tokens import generate_token

def login_user(email, password):
    user = get_user_by_email(email)
    if not user:
        return {'status': 'failure', 'message': 'User not found'}
    if not check_password(user['password'], password):
        return {'status': 'failure', 'message': 'Invalid credentials'}
    token = generate_token(user['id'])
    response = make_response(jsonify({'status': 'success', 'user_id': user['id']}))
    response.set_cookie('token', token, httponly=True, secure=True)
    return response

def register_user(firstName, lastName, dateOfBirth, country, email, password):
    hashed_password = hash_password(password)
    params = [firstName, lastName, dateOfBirth, country, email, hashed_password]
    try:
        call_procedure('GetUsers', params)
        return jsonify({'status': 'success'}), 201
    except Exception as e:
        return jsonify({'status': 'failure', 'message': str(e)})


def logout_user():
    response = make_response(jsonify({'status': 'success', 'message': 'Logged out successfully'}))
    response.set_cookie('token', '', expires=0)  # Clear the cookie
    return response

