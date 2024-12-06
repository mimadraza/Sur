from flask import session

def create_session(user_id):
    session['user_id'] = user_id

def destroy_session():
    session.pop('user_id', None)

def get_logged_in_user():
    return session.get('user_id')
