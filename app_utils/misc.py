import bcrypt

def hash_password(password):
    """Hash a given password"""
    
    return bcrypt.hashpw(password, bcrypt.gensalt())