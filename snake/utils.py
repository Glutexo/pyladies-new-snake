from collections import namedtuple


def struct(*args, **kwargs):
    Namedtuple = namedtuple(args[0], kwargs.keys())
    return Namedtuple(**kwargs)
