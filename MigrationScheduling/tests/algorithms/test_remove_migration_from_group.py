from unittest.mock import MagicMock
from MigrationScheduling.algorithms import remove_migration_from_group


def test_last_switch_in_group():
    migration = MagicMock()
    migration.get_switch = MagicMock(return_value='s3')
    group_const = MagicMock()
    group_const.remove_switch = MagicMock(side_effect=None)
    group_const.get_switches = MagicMock(return_value=set())
    consts_dict = {'c1': MagicMock(), 'g1': MagicMock(), 'g5': group_const}
    result_dict = remove_migration_from_group(migration, 'g5', consts_dict)
    migration.get_switch.assert_called_once()
    group_const.remove_switch.assert_called_once_with('s3', 1)
    group_const.get_switches.assert_called_once()
    assert result_dict == {'c1': consts_dict['c1'], 'g1': consts_dict['g1']}


def test_group_has_other_switches():
    migration = MagicMock()
    migration.get_switch = MagicMock(return_value='s7')
    group_const = MagicMock()
    group_const.remove_switch = MagicMock(side_effect=None)
    group_const.get_switches = MagicMock(return_value={'s0', 's1', 's4'})
    consts_dict = {'c2': MagicMock(), 'g0': group_const, 'g3': MagicMock()}
    result_dict = remove_migration_from_group(migration, 'g0', consts_dict)
    migration.get_switch.assert_called_once()
    group_const.remove_switch.assert_called_once_with('s7', 1)
    group_const.get_switches.assert_called_once()
    assert result_dict == {'c2': consts_dict['c2'],
                           'g0': group_const,
                           'g3': consts_dict['g3']}
