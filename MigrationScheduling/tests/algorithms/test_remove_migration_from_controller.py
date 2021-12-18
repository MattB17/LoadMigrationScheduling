from unittest.mock import MagicMock
from MigrationScheduling.algorithms import remove_migration_from_controller


def test_last_switch_on_controller():
    migration = MagicMock()
    migration.get_switch = MagicMock(return_value='s3')
    migration.get_load = MagicMock(return_value=1.5)
    control_const = MagicMock()
    control_const.remove_switch = MagicMock(side_effect=None)
    control_const.get_switches = MagicMock(return_value=set())
    consts_dict = {'c1': MagicMock(), 'c3': control_const, 'g0': MagicMock()}
    result_dict = remove_migration_from_controller(
        migration, 'c3', consts_dict)
    migration.get_switch.assert_called_once()
    migration.get_load.assert_called_once()
    control_const.remove_switch.assert_called_once_with('s3', 1.5)
    control_const.get_switches.assert_called_once()
    assert result_dict == {'c1': consts_dict['c1'], 'g0': consts_dict['g0']}


def test_controller_has_other_switches():
    migration = MagicMock()
    migration.get_switch = MagicMock(return_value='s7')
    migration.get_load = MagicMock(return_value=3.7)
    control_const = MagicMock()
    control_const.remove_switch = MagicMock(side_effect=None)
    control_const.get_switches = MagicMock(return_value={'s0', 's1', 's4'})
    consts_dict = {'c1': control_const, 'g3': MagicMock(), 'g4': MagicMock()}
    result_dict = remove_migration_from_controller(
        migration, 'c1', consts_dict)
    migration.get_switch.assert_called_once()
    migration.get_load.assert_called_once()
    control_const.remove_switch.assert_called_once_with('s7', 3.7)
    control_const.get_switches.assert_called_once()
    assert result_dict == {'c1': control_const,
                           'g3': consts_dict['g3'],
                           'g4': consts_dict['g4']}
