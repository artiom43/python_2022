__all__ = ["PasswordManagerError", "PasswordNotStoredError", "PasswordLengthError"]


class PasswordManagerError(ValueError):
    pass


class PasswordNotStoredError(PasswordManagerError):
    pass


class PasswordLengthError(PasswordManagerError):
    pass
