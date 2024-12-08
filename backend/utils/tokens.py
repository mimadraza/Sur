import jwt
import datetime

SECRET_KEY = 'SUR_APP'
# Generate a JWT token
def generate_token(user_id):
    # Set expiration time (1 hour) using timezone-aware datetime
    expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)

    # Generate the token, include user_id and expiration time
    token = jwt.encode(
        {
            'user_id': user_id,
            'exp': expiration_time
        },
        SECRET_KEY,  # Secret key to sign the token
        algorithm='HS256'  # Use the HS256 algorithm for signing
    )

    return token


def verify_token(provided_token):
    # Decode the token without raising exceptions (using options)
    decoded_token = jwt.decode(provided_token, SECRET_KEY, algorithms=['HS256'], options={"verify_exp": True})

    # Check if the token is successfully decoded and not expired
    if decoded_token:
        user_id = decoded_token.get('user_id')
        return True, user_id  # Token is valid, return user_id
    else:
        return False, 'Invalid or expired token'
