import pytest
from unittest.mock import patch
from MigrationScheduling.Data import Migration
from MigrationScheduling import exceptions as exc


VAL_STR = "MigrationScheduling.validation.validate_name"


@pytest.fixture(scope="function")
def migration():
    with patch(VAL_STR, side_effect=None) as mock_val:
        migration = Migration('s0', 'c3', 3.5)
    mock_val.assert_called_once_with('s0', 's', "Switch")
    return migration


def test_instantiation(migration):
    assert migration.get_switch() == 's0'
    assert migration.get_dst_controller() == 'c3'
    assert migration.get_load() == 3.5
    assert migration.get_groups() == set()

@patch(VAL_STR, side_effect=exc.InvalidName(""))
def test_invalid_name(mock_validate):
    with pytest.raises(exc.InvalidName):
        Migration('sw56', 'c1', 0.1)


def test_adding_groups(migration):
    migration.add_qos_group('g2')
    migration.add_qos_group('g5')
    migration.add_qos_group('g10')
    assert migration.get_groups() == {'g2', 'g5', 'g10'}


def test_is_in_group_gives_false(migration):
    assert not migration.is_in_group('g0')


def test_is_in_group_gives_true(migration):
    migration.add_qos_group('g2')
    migration.add_qos_group('g5')
    assert migration.is_in_group('g2')


def test_str_method_no_qos_groups(migration):
    migration_str = migration.__str__()
    assert migration_str == ("Migrate switch s0 to controller c3 with " +
                            "load of 3.50.\nNo QoS groups.")

def test_str_method_with_qos_groups(migration):
    migration._groups = {'g2', 'g5'}
    first_part = "Migrate switch s0 to controller c3 with load of 3.50.\n"
    second_part_1 = "QoS groups: g2 g5."
    second_part_2 = "QoS groups: g5 g2."
    migration_str = migration.__str__()
    assert migration_str in [first_part + second_part_1,
                             first_part + second_part_2]
