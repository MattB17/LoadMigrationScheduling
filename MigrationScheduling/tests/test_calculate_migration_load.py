import pytest
from unittest.mock import MagicMock
from MigrationScheduling.algorithms import calculate_migration_load


@pytest.fixture(scope="function")
def control_const():
    const = MagicMock()
    const.get_load_factor = MagicMock(return_value=0.7)
    return const


@pytest.fixture(scope="function")
def qos_const():
    const = MagicMock()
    const.get_load_factor = MagicMock(return_value=1.2)
    return const


def test_with_no_groups(control_const, qos_const):
    consts_dict = {'c0': control_const, 'g1': qos_const}
    migration = MagicMock()
    migration.get_groups = MagicMock(return_value=set())
    migration.get_dst_controller = MagicMock(return_value='c0')
    assert calculate_migration_load(migration, 'c0', consts_dict) == 0
    control_const.get_load_factor.assert_not_called()
    qos_const.get_load_factor.assert_not_called()


def test_with_one_group(control_const, qos_const):
    other_consts = [MagicMock(), MagicMock(), MagicMock()]
    for const in other_consts:
        const.get_load_factor = MagicMock()
    consts_dict = {'c1': control_const,
                   'c3': other_consts[0],
                   'g0': other_consts[1],
                   'g3': qos_const,
                   'g6': other_consts[2]}
    migration = MagicMock()
    migration.get_groups = MagicMock(return_value={'g3'})
    migration.get_dst_controller = MagicMock(return_value='c1')
    assert calculate_migration_load(migration, 'g3', consts_dict) == 0.7
    for const_name, const in consts_dict.items():
        if const_name == 'c1':
            const.get_load_factor.assert_called_once()
        else:
            const.get_load_factor.assert_not_called()


def test_with_multi_groups(control_const, qos_const):
    other_consts = [MagicMock() for _ in range(5)]
    other_consts[0].get_load_factor = MagicMock(return_value=2.3)
    for const in other_consts[1:]:
        const.get_load_factor = MagicMock()
    consts_dict = {'g0': qos_const,
                   'g3': other_consts[0],
                   'g7': other_consts[1],
                   'g11': other_consts[2],
                   'c1': other_consts[3],
                   'c2': other_consts[4],
                   'c5': control_const}
    migration = MagicMock()
    migration.get_groups = MagicMock(return_value={'g0', 'g3', 'g11'})
    migration.get_dst_controller = MagicMock(return_value='c5')
    assert calculate_migration_load(migration, 'g11', consts_dict) == 2.3
    for const in [control_const, qos_const, other_consts[0]]:
        const.get_load_factor.assert_called_once()
    for const in other_consts[1:]:
        const.get_load_factor.assert_not_called()
