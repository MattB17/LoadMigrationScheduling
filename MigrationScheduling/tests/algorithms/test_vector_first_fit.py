import pytest
from unittest.mock import call, patch, MagicMock
from MigrationScheduling.algorithms import vector_first_fit


SCHEDULE_STR = (
    "MigrationScheduling.algorithms.schedule_migration_in_earliest_round")
CAPS_STR = "MigrationScheduling.algorithms.utils.get_cap_dicts"

CONTROL_CAPS1 = {'c0': 3.4}
QOS_CAPS1 = {}
CONTROL_CAPS2 = {'c2': 11.5, 'c5': 3.7, 'c9': 6.8}
QOS_CAPS2 = {'g0': 1, 'g5': 2, 'g7': 3, 'g11': 1}


@pytest.fixture(scope="function")
def mock_data():
    return MagicMock()


@patch(CAPS_STR, return_value=({}, {}))
@patch(SCHEDULE_STR)
def test_with_no_migrations(mock_schedule, mock_caps, mock_data):
    mock_data.get_migrations = MagicMock(return_value={})
    assert vector_first_fit(mock_data, False) == 0
    mock_data.get_migrations.assert_called_once()
    mock_caps.assert_called_once_with(mock_data)
    mock_schedule.assert_not_called()


@patch(CAPS_STR, return_value=(CONTROL_CAPS1, QOS_CAPS1))
@patch(SCHEDULE_STR)
def test_with_one_migration(mock_schedule, mock_caps, mock_data):
    migration = [MagicMock()]
    mock_data.get_migrations = MagicMock(return_value={'s0': migration})
    round = MagicMock()
    mock_schedule.return_value = ([round], 1)
    assert vector_first_fit(mock_data, False) == 1
    mock_data.get_migrations.assert_called_once()
    mock_caps.assert_called_once_with(mock_data)
    mock_schedule.assert_called_once_with(
        [], 0, migration, CONTROL_CAPS1, QOS_CAPS1, False)

@patch(CAPS_STR, return_value=(CONTROL_CAPS2, QOS_CAPS2))
@patch(SCHEDULE_STR)
def test_with_multi_migrations(mock_schedule, mock_caps, mock_data):
    migrations = [MagicMock() for _ in range(5)]
    mock_dict = MagicMock()
    mock_data.get_migrations = MagicMock(return_value=mock_dict)
    mock_dict.values = MagicMock(return_value=migrations)
    rounds = [MagicMock() for _ in range(3)]
    mock_schedule.side_effect = ((rounds[:1], 1),
                                 (rounds[:2], 2),
                                 (rounds[:2], 2),
                                 (rounds[:2], 2),
                                 (rounds, 3))
    assert vector_first_fit(mock_data, True) == 3
    mock_data.get_migrations.assert_called_once()
    mock_dict.values.assert_called_once()
    mock_caps.assert_called_once_with(mock_data)
    schedule_calls = [
        call([], 0, migrations[0], CONTROL_CAPS2, QOS_CAPS2, True),
        call(rounds[:1], 1, migrations[1], CONTROL_CAPS2, QOS_CAPS2, True),
        call(rounds[:2], 2, migrations[2], CONTROL_CAPS2, QOS_CAPS2, True),
        call(rounds[:2], 2, migrations[3], CONTROL_CAPS2, QOS_CAPS2, True),
        call(rounds[:2], 2, migrations[4], CONTROL_CAPS2, QOS_CAPS2, True)]
    assert mock_schedule.call_count == 5
    mock_schedule.assert_has_calls(schedule_calls)
