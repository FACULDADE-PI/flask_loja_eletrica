import bcrypt


def hash_pass(password):
    """Hash a password for storing."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_pass(provided_password, stored_password):
    """Verify a stored password against one provided by user"""
    return bcrypt.checkpw(provided_password.encode("utf-8"), stored_password.encode("utf-8"))

