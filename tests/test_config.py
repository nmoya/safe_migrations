import pytest

from src.config import config_content


def test_config_file():
    config = config_content()
    assert isinstance(config, dict)
    assert "MONGO_URL" in config.keys()
    assert "MONGO_DATABASE" in config.keys()
    assert "MIGRATIONS_ROOT" in config.keys()
    assert "TEST_DATABASE" in config.keys()


if __name__ == "__main__":
    pytest.main(["-x", __file__])
