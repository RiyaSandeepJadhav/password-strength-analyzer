import secrets
import string


def generate_password(length=16):
    """
    Generate a cryptographically secure password.

    Parameters:
        length (int): Desired password length.

    Returns:
        str: Secure random password.
    """

    if length < 8:
        length = 8

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()-_=+[]{}<>?/"

    all_characters = lowercase + uppercase + digits + symbols

    # Ensure at least one character from each category
    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(symbols)
    ]

    # Fill remaining characters
    for _ in range(length - 4):
        password.append(secrets.choice(all_characters))

    # Secure shuffle
    secrets.SystemRandom().shuffle(password)

    return "".join(password)


if __name__ == "__main__":
    print(generate_password())