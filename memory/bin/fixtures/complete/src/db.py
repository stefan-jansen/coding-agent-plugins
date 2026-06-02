"""DB stub — exists so anchors in the index resolve to a real path."""


def connect(dsn):
    return {"dsn": dsn, "open": True}
