import difflib
import pprint
from functools import partial, reduce

import click
from pymongo.errors import OperationFailure

pp = pprint.PrettyPrinter(indent=1, width=60, compact=True)


def compose_impl(f, g):
    return lambda *a, **kw: f(g(*a, **kw))


def compose(*fs):
    return reduce(compose_impl, fs)


def identity(x):
    return x


def dict_changes(d1, d2):
    return d1.keys() - d2.keys()


import difflib
import pprint


def compare_dicts(d1, d2):
    return "\n" + "\n".join(difflib.unified_diff(pprint.pformat(d1).splitlines(), pprint.pformat(d2).splitlines()))


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
        click.echo_via_pager(pp.pformat(old))
        click.echo_via_pager(pp.pformat(new))


class CollectionDecorator:
    def __init__(self, db, collection):
        self.db = db
        self.collection = collection

    @staticmethod
    def _migrate_pipeline(db, pipeline):
        results = []
        transform_old = list
        transform_new = list
        transform_result = identity
        with db.client.start_session() as session:
            with session.start_transaction():
                try:
                    for operation in pipeline:
                        read_old_fn, read_new_fn, write_fn = operation()
                        old_data = transform_old(read_old_fn(session=session))
                        results.append(transform_result(write_fn(session=session)))
                        new_data = transform_new(read_new_fn(session=session))
                        print_diffs(old_data, new_data)
                        confirm = input("Confirm? [y/n] ")
                        if confirm != "y":
                            raise Exception
                except OperationFailure as ex:
                    print("OPERATION FAILURE")
                    print(ex)
                except Exception as ex:
                    print(ex)
                    print("Migration aborted by the user")
                    session.abort_transaction()

        return results

    def closure_updates(self, method, filter, update, **kwargs):
        def exec():
            read_old_fn = partial(self.collection.find, filter)
            read_new_fn = partial(self.collection.find, filter)
            write_fn = partial(getattr(self.collection, method), filter, update, **kwargs)
            return read_old_fn, read_new_fn, write_fn

        return exec

    def closure_deletes(self, method, filter, **kwargs):
        def exec():
            read_old_fn = partial(self.collection.find, filter)
            read_new_fn = partial(self.collection.find, filter)
            write_fn = partial(getattr(self.collection, method), filter, **kwargs)
            return read_old_fn, read_new_fn, write_fn

        return exec

    def closure_inserts(self, method, data, **kwargs):
        def exec():
            read_old_fn = lambda **kwargs: {}
            read_new_fn = lambda **kwargs: [data]
            write_fn = partial(getattr(self.collection, method), data, **kwargs)
            return read_old_fn, read_new_fn, write_fn

        return exec

    def __getattr__(self, name):
        updates = ["replace_one", "update_one", "update_many", "find_one_and_replace", "find_one_and_update"]
        deletes = ["delete_one", "delete_many", "find_one_and_delete"]
        inserts = ["insert_one", "insert_many"]
        if name in updates:
            return partial(self.closure_updates, name)
        elif name in deletes:
            return partial(self.closure_deletes, name)
        elif name in inserts:
            return partial(self.closure_inserts, name)
        if hasattr(self.collection, name):
            return getattr(self.collection, name)
        else:
            raise AttributeError


class DatabaseWrapper:
    def __init__(self, db):
        self.db = db

    def __getattr__(self, name):
        return CollectionDecorator(self.db, self.db.get_collection(name))
