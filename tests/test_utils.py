import pytest

from src.utils import compare_dicts, compose, identity, to_list


def test_compose():
    a = "1"
    composed = compose(to_list, int)
    assert composed(a) == [1]


def test_identity():
    assert identity(1) == 1


def test_compare_dicts():
    importers = {"El Salvador": 1234, "Nicaragua": 152, "Spain": 252}
    exporters = {"Spain": 252, "Germany": 251, "Italy": 1563}
    assert compare_dicts(importers, exporters).startswith("--- \n\n+++ \n\n@@ -1 +1 @@\n\n-")


if __name__ == "__main__":
    pytest.main(["-x", __file__])
