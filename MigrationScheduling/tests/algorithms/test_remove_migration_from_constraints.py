from unittest.mock import MagicMock
from MigrationScheduling.algorithms import remove_migration_from_constraints


def test_with_no_groups():
    consts_dict = {'c0': MagicMock(), 'c2': MagicMock(),
                   'g0': MagicMock(), 'g3': MagicMock(), 'g11': MagicMock()}
    for const in consts_dict.values():
        const.remove_switch = MagicMock(side_effect=None)
    consts_dict['c0'].get_switches = MagicMock(return_value={'s0', 's3'})
    for const_name in consts_dict.keys():
        if const_name != 'c0':
            consts_dict[const_name].get_swithces = MagicMock()
    migration = MagicMock()
    migration.get_switch = MagicMock(return_value='s2')
    migration.get_dst_controller = MagicMock(return_value='c0')
    migration.get_load = MagicMock(return_value=3.5)
    migration.get_groups = MagicMock(return_value=set())
    assert remove_migration_from_constraints(
        migration, consts_dict) == consts_dict
    consts_dict['c0'].remove_switch.assert_called_once_with('s2', 3.5)
    consts_dict['c0'].get_switches.assert_called_once()
    for const_name in consts_dict.keys():
        if const_name != 'c0':
            consts_dict[const_name].remove_switch.assert_not_called()
            consts_dict[const_name].get_switches.assert_not_called()
    migration.get_switch.assert_called_once()
    assert migration.get_dst_controller.call_count == 2
    migration.get_load.assert_called_once()
    migration.get_groups.assert_called_once()

def test_with_one_group():
    group_const = MagicMock()
    consts_dict = {'c1': MagicMock(), 'g0': MagicMock(), 'g2': group_const}
    for const in consts_dict.values():
        const.remove_switch = MagicMock(side_effect=None)
    consts_dict['c1'].get_switches = MagicMock(return_value={'s3'})
    consts_dict['g2'].get_swithces = MagicMock(return_value=set())
    consts_dict['g0'].get_switches = MagicMock()
    migration = MagicMock()
    migration.get_switch = MagicMock(return_value='s0')
    migration.get_dst_controller = MagicMock(return_value='c1')
    migration.get_load = MagicMock(return_value=11.7)
    migration.get_groups = MagicMock(return_value={'g2'})
    assert remove_migration_from_constraints(migration, consts_dict) == {
        'c1': consts_dict['c1'], 'g0': consts_dict['g0']}
    consts_dict['c1'].remove_switch.assert_called_once_with('s0', 11.7)
    group_const.remove_switch.assert_called_once_with('s0', 1)
    consts_dict['g0'].remove_switch.assert_not_called()
    consts_dict['c1'].get_switches.assert_called_once()
    consts_dict['g0'].get_switches.assert_not_called()
    group_const.get_switches.assert_called_once()
    assert migration.get_switch.call_count == 2
    assert migration.get_dst_controller.call_count == 2
    migration.get_load.assert_called_once()
    migration.get_groups.assert_called_once()

def test_with_multi_group():
    group_const = MagicMock()
    control_const = MagicMock()
    consts_dict = {'c1': control_const, 'c3': MagicMock(), 'c7': MagicMock(),
                   'g0': MagicMock(), 'g1': MagicMock(), 'g5': group_const}
    for const in consts_dict.values():
        const.remove_switch = MagicMock(side_effect=None)
    control_const.get_switches = MagicMock(return_value=set())
    group_const.get_swithces = MagicMock(return_value=set())
    consts_dict['c3'].get_switches = MagicMock()
    consts_dict['c7'].get_switches = MagicMock()
    consts_dict['g0'].get_switches = MagicMock(return_value={'s2', 's5'})
    consts_dict['g1'].get_switches = MagicMock(return_value={'s3'})
    migration = MagicMock()
    migration.get_switch = MagicMock(return_value='s7')
    migration.get_dst_controller = MagicMock(return_value='c1')
    migration.get_load = MagicMock(return_value=4.7)
    migration.get_groups = MagicMock(return_value={'g0', 'g1', 'g5'})
    assert remove_migration_from_constraints(migration, consts_dict) == {
        const_name: const for const_name, const in consts_dict.items()
        if const_name not in ['c1', 'g5']}
    control_const.remove_switch.assert_called_once_with('s7', 4.7)
    group_const.remove_switch.assert_called_once_with('s7', 1)
    consts_dict['c3'].remove_switch.assert_not_called()
    consts_dict['c7'].remove_switch.assert_not_called()
    consts_dict['g0'].remove_switch.assert_called_once_with('s7', 1)
    consts_dict['g1'].remove_switch.assert_called_once_with('s7', 1)
    control_const.get_switches.assert_called_once()
    group_const.get_switches.assert_called_once()
    consts_dict['c3'].get_switches.assert_not_called()
    consts_dict['c7'].get_switches.assert_not_called()
    consts_dict['g0'].get_switches.assert_called_once()
    consts_dict['g1'].get_switches.assert_called_once()
    assert migration.get_switch.call_count == 4
    assert migration.get_dst_controller.call_count == 3
    migration.get_load.assert_called_once()
    migration.get_groups.assert_called_once()
