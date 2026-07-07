"""Auth stub — exists so anchors in the index resolve to a real path."""


def login(user, token):
    return bool(user) and bool(token)
