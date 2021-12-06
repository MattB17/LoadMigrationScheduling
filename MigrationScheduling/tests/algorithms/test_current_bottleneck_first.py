import pytest
from unittest.mock import call, patch, MagicMock
from MigrationScheduling.algorithms import current_bottleneck_first


CAP_STR = "MigrationScheduling.algorithms.utils.get_cap_dicts"
CONST_STR = "MigrationScheduling.algorithms.utils.get_constraints_dict"
SELECT_STR = "MigrationScheduling.algorithms.select_bottleneck_migration"
SCHEDULE_STR = (
    "MigrationScheduling.algorithms.schedule_migration_in_earliest_round")
REMOVE_STR = (
    "MigrationScheduling.algorithms.remove_migration_from_constraints")

CONTROL_CAPS1 = {'c0': 3.7}
QOS_CAPS1 = {'g9': 1}
CONSTS_DICT1 = {'c0': MagicMock(), 'g9': MagicMock()}

CONTROL_CAPS2 = {'c1': 1.7, 'c2': 3.4}
QOS_CAPS2 = {'g0': 1, 'g1': 3, 'g5': 1}
CONSTS_DICT2 = {'c1': MagicMock(),
                'c2': MagicMock(),
                'g0': MagicMock(),
                'g1': MagicMock(),
                'g5': MagicMock()}


@patch(REMOVE_STR)
@patch(SCHEDULE_STR)
@patch(SELECT_STR)
@patch(CONST_STR, return_value={})
@patch(CAP_STR, return_value=({}, {}))
def test_with_no_migrations(mock_caps, mock_consts, mock_select,
                            mock_schedule, mock_remove):
    mock_data = MagicMock()
    assert current_bottleneck_first(mock_data, 1) == 0
    mock_caps.assert_called_once_with(mock_data)
    mock_consts.assert_called_once_with(mock_data)
    mock_select.assert_not_called()
    mock_schedule.assert_not_called()
    mock_remove.assert_not_called()


@patch(REMOVE_STR)
@patch(SCHEDULE_STR)
@patch(SELECT_STR)
@patch(CONST_STR, return_value=CONSTS_DICT1)
@patch(CAP_STR, return_value=(CONTROL_CAPS1, QOS_CAPS1))
def test_with_one_migration(mock_caps, mock_consts, mock_select,
                            mock_schedule, mock_remove):
    mock_data = MagicMock()
    migration = MagicMock()
    round = MagicMock()
    mock_select.return_value = migration
    mock_schedule.return_value = ([round], 1)
    mock_remove.return_value = {}
    assert current_bottleneck_first(mock_data, 1) == 1
    mock_caps.assert_called_once_with(mock_data)
    mock_consts.assert_called_once_with(mock_data)
    mock_select.assert_called_once_with(mock_data, 1, CONSTS_DICT1)
    mock_schedule.assert_called_once_with(
        [], 0, migration, CONTROL_CAPS1, QOS_CAPS1)
    mock_remove.assert_called_once_with(migration, CONSTS_DICT1)


@patch(REMOVE_STR)
@patch(SCHEDULE_STR)
@patch(SELECT_STR)
@patch(CONST_STR, return_value=CONSTS_DICT2)
@patch(CAP_STR, return_value=(CONTROL_CAPS2, QOS_CAPS2))
def test_with_multi_migrations(mock_caps, mock_consts, mock_select,
                               mock_schedule, mock_remove):
    mock_data = MagicMock()
    migrations = tuple(MagicMock() for _ in range(5))
    dict1 = {const_name: const for const_name, const in CONSTS_DICT2.items()}
    dict2 = {'c1': CONSTS_DICT2['c1'], 'c2': CONSTS_DICT2['c2'],
             'g0': CONSTS_DICT2['g0'], 'g1': CONSTS_DICT2['g1']}
    dict3 = {'c1': CONSTS_DICT2['c1'], 'g1': CONSTS_DICT2['g1']}
    dict4 = {'g1': CONSTS_DICT2['g1']}
    rounds = [MagicMock() for _ in range(3)]
    mock_select.side_effect = migrations
    mock_schedule.side_effect = ((rounds[:1], 1),
                                 (rounds[:1], 1),
                                 (rounds[:1], 1),
                                 (rounds[:2], 2),
                                 (rounds, 3))
    mock_remove.side_effect = (dict1, dict2, dict3, dict4, {})
    assert current_bottleneck_first(mock_data, 2) == 3
    mock_caps.assert_called_once_with(mock_data)
    mock_consts.assert_called_once_with(mock_data)
    dicts = [CONSTS_DICT2, dict1, dict2, dict3, dict4]
    select_calls = [call(mock_data, 2, const_dict) for const_dict in dicts]
    assert mock_select.call_count == 5
    mock_select.assert_has_calls(select_calls)
    schedule_calls = [
        call([], 0, migrations[0], CONTROL_CAPS2, QOS_CAPS2),
        call(rounds[:1], 1, migrations[1], CONTROL_CAPS2, QOS_CAPS2),
        call(rounds[:1], 1, migrations[2], CONTROL_CAPS2, QOS_CAPS2),
        call(rounds[:1], 1, migrations[3], CONTROL_CAPS2, QOS_CAPS2),
        call(rounds[:2], 2, migrations[4], CONTROL_CAPS2, QOS_CAPS2)]
    assert mock_schedule.call_count == 5
    mock_schedule.assert_has_calls(schedule_calls)
    remove_calls = [call(migrations[i], dicts[i]) for i in range(5)]
    assert mock_remove.call_count == 5
    mock_remove.assert_has_calls(remove_calls)
