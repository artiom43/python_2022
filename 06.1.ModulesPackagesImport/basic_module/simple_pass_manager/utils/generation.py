__all__ = [
                'generate_password', 'generate_urlsafe_password'
            ]

# from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
import string
import secrets
# import hashlib

# from cryptography.fernet import Fernet
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


LETTERS = string.ascii_letters
DIGITS = string.digits
SPECIAL = '-_+#!@$%^:;*()[]'


def generate_password(pass_len: int = 32, letters: bool = True, digits: bool = True, special: bool = True) -> str:
    """Generate pass with alphabet control"""
    assert pass_len > 0

    alphabet: str = ''
    if letters:
        alphabet += LETTERS
    if digits:
        alphabet += DIGITS
    if special:
        alphabet += SPECIAL

    assert alphabet, 'Can not generate password with empty alphabet'

    return ''.join(secrets.choice(alphabet) for i in range(pass_len))


def generate_urlsafe_password(pass_len: int = 32) -> str:
    """Generate url-safe pass"""
    assert pass_len > 0
    return secrets.token_urlsafe(pass_len)[:pass_len]
