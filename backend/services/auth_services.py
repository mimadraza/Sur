from flask import make_response, jsonify
from backend.db.queries import get_user_by_email, call_procedure, create_artist, get_artist_by_email
from backend.utils.hashing import hash_password, check_password
from backend.utils.tokens import generate_token


def login_user(email, password):
    user = get_user_by_email(email)
    if not user:
        return jsonify({'status': 'failure', 'message': 'User not found'})
    if not check_password(user['password_hash'], password):
        return jsonify({'status': 'failure', 'message': 'Invalid credentials'})

    token = generate_token(user['user_id'])
    response_data = {'status': 'success', 'user_id': user['user_id']}
    response = make_response(jsonify(response_data), 200)
    response.set_cookie('token', token, httponly=True, secure=True)
    return response  # Response object is returned with data and headers


def register_user(first_name, last_name, date_of_birth, country, email, password):
    # Check if the email already exists in the database
    existing_user = get_user_by_email(email)
    if existing_user:
        return {'status': 'failure', 'message': 'Email already in use'}

    # Ensure date_of_birth is in the correct format
    if not isinstance(date_of_birth, str):
        return {'status': 'failure', 'message': 'Invalid date format for date of birth'}

    hashed_password = hash_password(password)
    params = [first_name, last_name, email, hashed_password, date_of_birth, country]

    try:
        # Call procedure to insert user into the database
        call_procedure('create_user', params)
        return {'status': 'success', 'message': 'User registered successfully'}
    except Exception as e:
        return {'status': 'failure', 'message': str(e)}


def logout_user():
    response_data = {'status': 'success', 'message': 'Logged out successfully'}
    response = make_response(jsonify(response_data))
    response.set_cookie('token', '', expires=0)  # Clear the cookie
    return response  # Response object is returned with data and headers


# Artist Login Logic
def login_artist(email, password):
    artist = get_artist_by_email(email)
    if not artist:
        return jsonify({'status': 'failure', 'message': 'Artist not found'})
    if not check_password(artist['password_hash'], password):  # Verify password hash
        return jsonify({'status': 'failure', 'message': 'Invalid credentials'})

    token = generate_token(artist['artist_id'])
    response_data = {'status': 'success', 'artist_id': artist['artist_id']}
    response = make_response(jsonify(response_data), 200)
    response.set_cookie('token', token, httponly=True, secure=True)
    return response  # Response object is returned with data and headers


# Artist Registration Logic
def register_artist(first_name, last_name, email, password, date_of_birth, bio, country):
    # Hash the password
    hashed_password = hash_password(password)

    try:
        # Insert the artist into the DB
        create_artist(first_name, last_name, email, hashed_password, date_of_birth, bio, country)

        # Log the artist in immediately after registration
        return login_artist(email, password)  # login_artist returns a response object with data and headers
    except Exception as e:
        return jsonify({'status': 'failure', 'message': str(e)})


# Artist Logout Logic
def logout_artist():
    response_data = {'status': 'success', 'message': 'Logged out successfully'}
    response = make_response(jsonify(response_data))
    response.set_cookie('token', '', expires=0)  # Clear the token cookie
    return response  # Response object is returned with data and headers
