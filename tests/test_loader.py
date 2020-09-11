import collections
from marshal import load

import pytest

from src.loader import import_method_by_module_str, load_migration_files, load_migration_modules

ROOT = "tests/test_migration"


def test_migration_root_traversal():
    migrations = load_migration_files(ROOT)
    assert len(migrations) == 1
    assert migrations[0].startswith(ROOT)


def test_load_migration_modules():
    migrations = load_migration_modules(ROOT)
    assert len(migrations) == 1
    root_module = ROOT.replace("/", ".")
    assert migrations[0].startswith(root_module)


def test_import_by_string():
    migrations = load_migration_modules(ROOT)
    assert len(migrations) == 1
    migration_fn = import_method_by_module_str(migrations[0], "up")
    # Ensure that it properly loaded the fixture function
    assert hasattr(migration_fn, "__call__")


if __name__ == "__main__":
    pytest.main(["-x", __file__])
