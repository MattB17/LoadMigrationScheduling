import pytest
from unittest.mock import patch, MagicMock
from MigrationScheduling.utils import get_load_contribution


@pytest.fixture(scope="function")
def mock_migration():
    migration = MagicMock()
    migration.get_load = MagicMock(return_value=3.7)
    return migration


def test_resilience_with_match(mock_migration):
    mock_migration.uses_controller = MagicMock(return_value=True)
    mock_migration.get_dst_controller = MagicMock()
    assert get_load_contribution(mock_migration, "c2", True) == 3.7
    mock_migration.uses_controller.assert_called_once_with("c2")
    mock_migration.get_load.assert_called_once()
    mock_migration.get_dst_controller.assert_not_called()


def test_resilience_without_match(mock_migration):
    mock_migration.uses_controller = MagicMock(return_value=False)
    mock_migration.get_dst_controller = MagicMock()
    assert round(get_load_contribution(mock_migration, "c7", True), 1) == 0.0
    mock_migration.uses_controller.assert_called_once_with("c7")
    mock_migration.get_load.assert_not_called()
    mock_migration.get_dst_controller.assert_not_called()


def test_no_resilience_with_match(mock_migration):
    mock_migration.uses_controller = MagicMock()
    mock_migration.get_dst_controller = MagicMock(return_value="c1")
    assert get_load_contribution(mock_migration, "c1", False) == 3.7
    mock_migration.uses_controller.assert_not_called()
    mock_migration.get_load.assert_called_once()
    mock_migration.get_dst_controller.assert_called_once()


def test_no_resilience_without_match(mock_migration):
    mock_migration.uses_controller = MagicMock()
    mock_migration.get_dst_controller = MagicMock(return_value="c5")
    assert round(get_load_contribution(mock_migration, "c0", False), 1) == 0.0
    mock_migration.uses_controller.assert_not_called()
    mock_migration.get_load.assert_not_called()
    mock_migration.get_dst_controller.assert_called_once()
