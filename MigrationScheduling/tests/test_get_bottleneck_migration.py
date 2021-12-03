import pytest
from unittest.mock import call, patch, MagicMock
from MigrationScheduling.algorithms import get_bottleneck_migration


CALC_STR = "MigrationScheduling.algorithms.calculate_migration_load"


@pytest.fixture(scope="function")
def mock_data():
    return MagicMock()


@patch(CALC_STR, side_effect=None)
def test_with_no_migrations(mock_calc, mock_data):
    mock_data.get_migration = MagicMock()
    assert get_bottleneck_migration([], 'c2', mock_data, {}) is None
    mock_data.get_migration.assert_not_called()
    mock_calc.assert_not_called()


@patch(CALC_STR, return_value=1.2)
def test_with_one_migration(mock_calc, mock_data):
    mock_migration = MagicMock()
    mock_data.get_migration = MagicMock(return_value=mock_migration)
    consts_dict = {'c1': MagicMock(), 'g0': MagicMock(), 'g3': MagicMock()}
    assert get_bottleneck_migration(
        {'s1'}, 'g0', mock_data, consts_dict) == mock_migration
    mock_data.get_migration.assert_called_once_with('s1')
    mock_calc.assert_called_once_with(mock_migration, 'g0', consts_dict)


@patch(CALC_STR, side_effect=(0.7, 2.1, 1.5))
def test_with_multi_migrations(mock_calc, mock_data):
    migrations = (MagicMock(), MagicMock(), MagicMock())
    mock_data.get_migration = MagicMock(side_effect=migrations)
    consts_dict = {'c0': MagicMock(),
                   'c1': MagicMock(),
                   'g1': MagicMock(),
                   'g3': MagicMock(),
                   'g7': MagicMock()}
    assert get_bottleneck_migration(
        ['s3', 's9', 's11'], 'g3', mock_data, consts_dict) == migrations[1]
    migration_calls = [call('s3'), call('s9'), call('s11')]
    assert mock_data.get_migration.call_count == 3
    mock_data.get_migration.assert_has_calls(migration_calls)
    calc_calls = [call(migration, 'g3', consts_dict)
                  for migration in migrations]
    assert mock_calc.call_count == 3
    mock_calc.assert_has_calls(calc_calls)
