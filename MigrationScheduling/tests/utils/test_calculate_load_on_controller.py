import pytest
from unittest.mock import MagicMock
from MigrationScheduling.utils import calculate_load_on_controller


@pytest.fixture(scope="function")
def mock_migration():
    migration = MagicMock()
    migration.uses_controller = MagicMock(return_value=True)
    migration.get_load = MagicMock(return_value=6.75)
    return migration


def test_no_migrations():
    assert calculate_load_on_controller('c5', []) == 0


def test_one_migration(mock_migration):
    assert round(
        calculate_load_on_controller('c2', [mock_migration]), 2) == 6.75
    mock_migration.uses_controller.assert_called_once()
    mock_migration.get_load.assert_called_once()

def test_multiple_migration(mock_migration):
    migrations = [mock_migration] + [MagicMock() for _ in range(2)]
    migrations[1].uses_controller = MagicMock(return_value=False)
    migrations[1].get_load = MagicMock()
    migrations[2].uses_controller = MagicMock(return_value=True)
    migrations[2].get_load = MagicMock(return_value=3.51)
    assert round(calculate_load_on_controller('c2', migrations), 2) == 10.26
    for migration in migrations:
        migration.uses_controller.assert_called_once()
    migrations[0].get_load.assert_called_once()
    migrations[1].get_load.assert_not_called()
    migrations[2].get_load.assert_called_once()
