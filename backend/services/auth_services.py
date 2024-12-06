from db.queries import get_user_by_username
from utils.hashing import check_password
from utils.tokens import generate_token

def login_user(username, password):
    user = get_user_by_username(username)
    if not user:
        return {'status': 'failure', 'message': 'User not found'}
    if not check_password(user['password'], password):
        return {'status': 'failure', 'message': 'Invalid credentials'}
    token = generate_token(user['id'])
    return {'status': 'success', 'token': token, 'user_id': user['id']}