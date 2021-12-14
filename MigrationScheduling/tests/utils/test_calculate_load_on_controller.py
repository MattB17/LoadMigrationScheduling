import pytest
from unittest.mock import call, MagicMock, patch
from MigrationScheduling.utils import calculate_load_on_controller


CONTRIB_STR = "MigrationScheduling.utils.get_load_contribution"


@patch(CONTRIB_STR)
def test_no_migrations(mock_contrib):
    assert calculate_load_on_controller('c5', [], True) == 0
    mock_contrib.assert_not_called()


@patch(CONTRIB_STR, return_value=6.75)
def test_one_migration(mock_contrib):
    mock_migration = MagicMock()
    assert round(calculate_load_on_controller(
        'c2', [mock_migration], False), 2) == 6.75
    mock_contrib.assert_called_once_with(mock_migration, "c2", False)

@patch(CONTRIB_STR, side_effect=(6.75, 0.00, 3.51))
def test_multiple_migration(mock_contrib):
    migrations = [MagicMock() for _ in range(3)]
    assert round(calculate_load_on_controller(
        'c4', migrations, True), 2) == 10.26
    contrib_calls = [call(migration, 'c4', True) for migration in migrations]
    assert mock_contrib.call_count == 3
    mock_contrib.assert_has_calls(contrib_calls)
