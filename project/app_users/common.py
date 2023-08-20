from string import ascii_letters, digits
from random import choices


def generate_invite_code():
    """
    Function for generating invite code of users.
    """

    characters = ascii_letters + digits
    invite_code = ''.join(choices(characters, k=6))
    return invite_code
