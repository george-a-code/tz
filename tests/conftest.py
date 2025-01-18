import pytest
from pathlib import Path

from tests.constants import TIMEZONE_NAMES


@pytest.fixture(scope="session")
def test_dir() -> Path:
    """Fixture to provide the test directory path."""
    return Path(__file__).resolve().parent


@pytest.fixture(scope="function")
def test_db_path(test_dir):
    """Fixture to provide the test database path."""
    test_db_path = test_dir / "test.db"
    yield test_db_path
    if test_db_path.exists():
        test_db_path.unlink()


@pytest.fixture(scope="session")
def timezone_example_list():
    return TIMEZONE_NAMES
