from .decode import parse


def loads(json):
    return parse(json)