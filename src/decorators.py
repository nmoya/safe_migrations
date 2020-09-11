from functools import partial

from pymongo.errors import OperationFailure

from src.utils import compose, print_diffs, to_list


class CollectionDecorator:
    def __init__(self, db, collection):
        self.db = db
        self.collection = collection

    @staticmethod
    def _migrate_pipeline(db, pipeline):
        results = []
        with db.client.start_session() as session:
            with session.start_transaction():
                try:
                    for operation in pipeline:
                        read_old_fn, read_new_fn, write_fn = operation()
                        old_data = read_old_fn(session=session)
                        results.append(write_fn(session=session))
                        new_data = read_new_fn(session=session)
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
            read_old_fn = compose(to_list, partial(self.collection.find, filter))
            read_new_fn = compose(to_list, partial(self.collection.find, filter))
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
