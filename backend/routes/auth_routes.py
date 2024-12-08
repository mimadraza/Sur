from flask import Blueprint, request, jsonify
from backend.services.auth_services import login_user, login_artist, register_artist, logout_artist, register_user, \
    logout_user

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/user/login', methods=['POST'])
def login():
    data = request.json
    response_data = login_user(data.get('email'), data.get('password'))

    # Check if response is a dictionary (success data)
    if isinstance(response_data, dict):
        return jsonify(response_data)  # Return the data as JSON if it's a dictionary
    else:
        return response_data


@auth_blueprint.route('/user/register', methods=['POST'])
def user_register():
    data = request.json
    # Extract the correct fields
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    dob = data.get('dob')  # Ensure this is a valid date string, e.g., '1990-01-01'
    country = data.get('country')
    email = data.get('email')
    password = data.get('password')

    # Check if dob is valid (date format validation can be done here as well)
    if not dob:
        return jsonify({'status': 'failure', 'message': 'Date of birth is required'}), 400

    # Call the register_user function with correct parameters
    response_data = register_user(first_name, last_name, dob, country, email, password)

    if isinstance(response_data, dict):  # Return response as JSON
        return jsonify(response_data)
    else:
        return response_data

@auth_blueprint.route('/user/logout', methods=['POST'])
def logout():
    response = logout_user()
    return response

@auth_blueprint.route('/artist/login', methods=['POST'])
def artist_login():  # Renamed to avoid conflict
    data = request.json
    response = login_artist(data.get('email'), data.get('password'))
    return response  # Now login_artist() will return the response with headers and data

@auth_blueprint.route('/artist/register', methods=['POST'])
def artist_register():  # Renamed to avoid conflict
    data = request.json
    response = register_artist(
        data.get('first_name'),
        data.get('last_name'),
        data.get('email'),
        data.get('password'),
        data.get('date_of_birth'),
        data.get('bio'),
        data.get('country')
    )
    return response  # Now register_artist() will return the response with headers and data

@auth_blueprint.route('/artist/logout', methods=['POST'])
def artist_logout():  # Renamed to avoid conflict
    response = logout_artist()
    return response  # logout_artist() now returns the response with proper headers
