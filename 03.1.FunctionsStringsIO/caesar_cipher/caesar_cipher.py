import string


def caesar_encrypt(message: str, n: int) -> str:
    """Encrypt message using caesar cipher

    :param message: message to encrypt
    :param n: shift
    :return: encrypted message
    """
    alphabet_lw = string.ascii_lowercase
    alphabet_up = string.ascii_uppercase
    encrypted_message = ""
    for letter in message:
        if letter in alphabet_lw:
            encrypted_message = encrypted_message + alphabet_lw[(alphabet_lw.index(letter) + n) % 26]
        elif letter in alphabet_up:
            encrypted_message = encrypted_message + alphabet_up[(alphabet_up.index(letter) + n) % 26]
        else:
            encrypted_message = encrypted_message + letter
    return encrypted_message
