import hashlib
import os
import hmac

def hash_password(password):
    salt = os.urandom(16)
    hash_object = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 10000)
    return salt + hash_object

def verify_password(real, given):
    salt = real[:16]
    real_hash = real[16:]
    given_hash = hashlib.pbkdf2_hmac('sha256', given.encode(), salt, 10000)

    return hmac.compare_digest(real_hash, given_hash)
