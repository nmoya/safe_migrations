import difflib
import pprint
from functools import reduce

import click

pp = pprint.PrettyPrinter(indent=1, width=60, compact=True)


class Singleton(type):
    """
    Extracted from Beazley, David. Python Cookbook (p. 357). O'Reilly Media. Kindle Edition.
    """

    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


def _compose(f, g):
    return lambda *a, **kw: f(g(*a, **kw))


def compose(*fs):
    return reduce(_compose, fs)


def to_list(value):
    return [value]


def identity(x):
    return x


def compare_dicts(d1, d2):
    d1_lines = pprint.pformat(d1).splitlines()
    d2_lines = pprint.pformat(d2).splitlines()
    return "\n".join(difflib.unified_diff(d1_lines, d2_lines))


def pformat(any_object):
    return pp.pformat(any_object)


def print_diffs(old, new):
    if isinstance(old, list) and isinstance(new, list):
        outputs = []
        if not old:  # data was inserted
            old = [{}]
        if not new:  # data was deleted
            new = [{}]
        # data was updated
        for n, g in zip(old, new):
            outputs.append(compare_dicts(n, g))
        click.echo_via_pager("\n".join(outputs))
    else:
        click.echo_via_pager(pformat(old))
        click.echo_via_pager(pformat(new))
