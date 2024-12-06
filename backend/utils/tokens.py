import secrets

def generate_token():
    return secrets.token_hex(32)  # 64-character random token

# Verify token (you'll need a database to match tokens)
def verify_token(stored_token, provided_token):
    return stored_token == provided_token
