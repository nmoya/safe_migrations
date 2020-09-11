import pytest

from src.config import TEST_DATABASE


def test_database_fixture(db):
    films = list(db().movies.find({}))
    assert len(films) > 0


def test_test_database_initialization(db):
    assert db.database_name == TEST_DATABASE


if __name__ == "__main__":
    pytest.main(["-x", __file__])
