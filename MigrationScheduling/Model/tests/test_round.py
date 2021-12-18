import io
import sys
import pytest
from unittest.mock import call, MagicMock
from MigrationScheduling.Model import Round


@pytest.fixture(scope="function")
def empty_round():
    return Round(0, {}, {})

@pytest.fixture(scope="function")
def simple_round():
    return Round(1, {'c0': 3.8}, {'g0': 1})

@pytest.fixture(scope="function")
def complex_round():
    return Round(0,
                 {'c0': 5.9, 'c1': 2.7, 'c2': 11.9},
                 {'g0': 2, 'g1': 1, 'g2': 5, 'g3': 0})

@pytest.fixture(scope="function")
def no_group_migration():
    migration = MagicMock()
    migration.get_src_controller = MagicMock(return_value='c3')
    migration.get_dst_controller = MagicMock(return_value='c0')
    migration.get_load = MagicMock(return_value=2.1)
    migration.get_groups = MagicMock(return_value=set())
    migration.get_switch = MagicMock(return_value='s0')
    return migration

@pytest.fixture(scope="function")
def simple_migration():
    migration = MagicMock()
    migration.get_src_controller = MagicMock(return_value='c7')
    migration.get_dst_controller = MagicMock(return_value='c2')
    migration.get_load = MagicMock(return_value=10.5)
    migration.get_groups = MagicMock(return_value={'g0'})
    migration.get_switch = MagicMock(return_value='s3')
    return migration

@pytest.fixture(scope="function")
def complex_migration():
    migration = MagicMock()
    migration.get_src_controller = MagicMock(return_value='c0')
    migration.get_dst_controller = MagicMock(return_value='c1')
    migration.get_load = MagicMock(return_value=1.0)
    migration.get_groups = MagicMock(return_value={'g0', 'g1', 'g2'})
    migration.get_switch = MagicMock(return_value='s1')
    return migration


def test_instantiation_empty_round(empty_round):
    assert empty_round.get_round_number() == 0
    assert empty_round.get_remaining_controller_capacities() == {}
    assert empty_round.get_remaining_qos_capacities() == {}
    assert empty_round.get_scheduled_migrations() == set()

def test_instantiation_simple_round(simple_round):
    assert simple_round.get_round_number() == 1
    assert simple_round.get_remaining_controller_capacities() == {'c0': 3.8}
    assert simple_round.get_remaining_qos_capacities() == {'g0': 1}
    assert simple_round.get_scheduled_migrations() == set()

def test_instantiation_complex_round(complex_round):
    assert complex_round.get_round_number() == 0
    assert complex_round.get_remaining_controller_capacities() == {
        'c0': 5.9, 'c1': 2.7, 'c2': 11.9}
    assert complex_round.get_remaining_qos_capacities() == {
        'g0': 2, 'g1': 1, 'g2': 5, 'g3': 0}
    assert complex_round.get_scheduled_migrations() == set()

def test_within_controller_cap_gives_true(simple_round, complex_round):
    assert simple_round._within_controller_cap('c0', 2.5)
    assert complex_round._within_controller_cap('c1', 2.7)

def test_within_controller_cap_gives_false(simple_round, complex_round):
    assert not simple_round._within_controller_cap('c1', 1.1)
    assert not complex_round._within_controller_cap('c2', 12.0)

def test_within_qos_caps_simple(empty_round, simple_round):
    assert empty_round._within_qos_caps(set())
    assert simple_round._within_qos_caps({'g0'})
    assert not simple_round._within_qos_caps({'g3'})

def test_within_qos_caps_complex(simple_round, complex_round):
    assert not simple_round._within_qos_caps({'g0', 'g3'})
    assert complex_round._within_qos_caps({'g0', 'g1', 'g2'})
    assert not complex_round._within_qos_caps({'g0', 'g3'})

def test_below_gives_false_no_resiliency(simple_round, no_group_migration):
    simple_round._within_controller_cap = MagicMock(return_value=False)
    assert not simple_round._below_controller_caps(no_group_migration, False)
    no_group_migration.get_src_controller.assert_not_called()
    no_group_migration.get_dst_controller.assert_called_once()
    no_group_migration.get_load.assert_called_once()
    simple_round._within_controller_cap.assert_called_once_with('c0', 2.1)

def test_below_gives_true_no_resiliency(simple_round, simple_migration):
    simple_round._within_controller_cap = MagicMock(return_value=True)
    assert simple_round._below_controller_caps(simple_migration, False)
    simple_migration.get_src_controller.assert_not_called()
    simple_migration.get_dst_controller.assert_called_once()
    simple_migration.get_load.assert_called_once()
    simple_round._within_controller_cap.assert_called_once_with('c2', 10.5)

def test_above_dst_with_resiliency(complex_round, complex_migration):
    complex_round._within_controller_cap = MagicMock(return_value=False)
    assert not complex_round._below_controller_caps(complex_migration, True)
    complex_migration.get_src_controller.assert_not_called()
    complex_migration.get_dst_controller.assert_called_once()
    complex_migration.get_load.assert_called_once()
    complex_round._within_controller_cap.assert_called_once_with('c1', 1.0)

def test_above_src_with_resiliency(complex_round, complex_migration):
    complex_round._within_controller_cap = MagicMock(
        side_effect=(True, False))
    assert not complex_round._below_controller_caps(complex_migration, True)
    complex_migration.get_src_controller.assert_called_once()
    complex_migration.get_dst_controller.assert_called_once()
    assert complex_migration.get_load.call_count == 2
    within_calls = [call('c1', 1.0), call('c0', 1.0)]
    assert complex_round._within_controller_cap.call_count == 2
    complex_round._within_controller_cap.assert_has_calls(within_calls)

def test_below_gives_true_with_resiliency(simple_round, simple_migration):
    simple_round._within_controller_cap = MagicMock(side_effect=(True, True))
    assert simple_round._below_controller_caps(simple_migration, True)
    simple_migration.get_src_controller.assert_called_once()
    simple_migration.get_dst_controller.assert_called_once()
    assert simple_migration.get_load.call_count == 2
    within_calls = [call('c2', 10.5), call('c7', 10.5)]
    assert simple_round._within_controller_cap.call_count == 2
    simple_round._within_controller_cap.assert_has_calls(within_calls)

def test_reduce_controller_cap_simple(simple_round):
    simple_round._reduce_controller_cap('c0', 2.0)
    rem_caps = simple_round.get_remaining_controller_capacities()
    assert set(rem_caps.keys()) == {'c0'}
    assert set(round(cap, 1) for cap in rem_caps.values()) == {1.8}

def test_reduce_controller_cap_complex(complex_round):
    complex_round._reduce_controller_cap('c1', 2.7)
    rem_caps = complex_round.get_remaining_controller_capacities()
    assert set(rem_caps.keys()) == {'c0', 'c1', 'c2'}
    assert set(round(cap, 1) for cap in rem_caps.values()) == {5.9, 0.0, 11.9}

def test_reduce_qos_caps_no_groups(empty_round):
    empty_round._reduce_qos_caps(set())
    assert empty_round.get_remaining_qos_capacities() == {}

def test_reduce_qos_caps_simple(simple_round):
    simple_round._reduce_qos_caps({'g0'})
    assert simple_round.get_remaining_qos_capacities() == {'g0': 0}

def test_reduce_qos_caps_complex(complex_round):
    complex_round._reduce_qos_caps({'g0', 'g1', 'g2'})
    assert complex_round.get_remaining_qos_capacities() == {
        'g0': 1, 'g1': 0, 'g2': 4, 'g3': 0}

def test_can_schedule_migration_no_groups(simple_round, no_group_migration):
    simple_round._below_controller_caps = MagicMock(return_value=True)
    simple_round._within_qos_caps = MagicMock(return_value=True)
    assert simple_round.can_schedule_migration(no_group_migration, False)
    no_group_migration.get_groups.assert_called_once()
    simple_round._below_controller_caps.assert_called_once_with(
        no_group_migration, False)
    simple_round._within_qos_caps.assert_called_once_with(set())

def test_can_schedule_migration_with_group(complex_round, simple_migration):
    complex_round._below_controller_caps = MagicMock(return_value=True)
    complex_round._within_qos_caps = MagicMock(return_value=True)
    assert complex_round.can_schedule_migration(simple_migration, True)
    simple_migration.get_groups.assert_called_once()
    complex_round._below_controller_caps.assert_called_once_with(
        simple_migration, True)
    complex_round._within_qos_caps.assert_called_once_with({'g0'})

def test_can_schedule_migration_with_multi_groups(complex_round,
                                                  complex_migration):
    complex_round._below_controller_caps = MagicMock(return_value=True)
    complex_round._within_qos_caps = MagicMock(return_value=True)
    assert complex_round.can_schedule_migration(complex_migration, False)
    complex_migration.get_groups.assert_called_once()
    complex_round._below_controller_caps.assert_called_once_with(
        complex_migration, False)
    complex_round._within_qos_caps.assert_called_once_with({'g0', 'g1', 'g2'})

def test_cant_schedule_controller_cap_too_low(simple_round):
    migration = MagicMock()
    migration.get_groups = MagicMock(return_value={'g0'})
    simple_round._below_controller_caps = MagicMock(return_value=False)
    simple_round._within_qos_caps = MagicMock(return_value=True)
    assert not simple_round.can_schedule_migration(migration, False)
    migration.get_groups.assert_called_once()
    simple_round._below_controller_caps.assert_called_once_with(
        migration, False)
    simple_round._within_qos_caps.assert_called_once_with({'g0'})

def test_cant_schedule_group_cap_too_low(complex_round):
    migration = MagicMock()
    migration.get_groups = MagicMock(return_value={'g3'})
    complex_round._below_controller_caps = MagicMock(return_value=True)
    complex_round._within_qos_caps = MagicMock(return_value=False)
    assert not complex_round.can_schedule_migration(migration, True)
    migration.get_groups.assert_called_once()
    complex_round._below_controller_caps.assert_called_once_with(
        migration, True)
    complex_round._within_qos_caps.assert_called_once_with({'g3'})


def test_cant_schedule_both_too_low(complex_round):
    migration = MagicMock()
    migration.get_groups = MagicMock(return_value={'g0', 'g1', 'g2', 'g3'})
    complex_round._below_controller_caps = MagicMock(return_value=False)
    complex_round._within_qos_caps = MagicMock(return_value=False)
    assert not complex_round.can_schedule_migration(migration, True)
    migration.get_groups.assert_called_once()
    complex_round._below_controller_caps.assert_called_once_with(
        migration, True)
    complex_round._within_qos_caps.assert_called_once_with(
        {'g0', 'g1', 'g2', 'g3'})

def test_schedule_migration_no_groups(simple_round, no_group_migration):
    simple_round._schedule_for_controllers = MagicMock(side_effect=None)
    simple_round._reduce_qos_caps = MagicMock(side_effect=None)
    simple_round.schedule_migration(no_group_migration, False)
    assert simple_round._migrations == {'s0'}
    no_group_migration.get_groups.assert_called_once()
    no_group_migration.get_switch.assert_called_once()
    simple_round._schedule_for_controllers.assert_called_once_with(
        no_group_migration, False)
    simple_round._reduce_qos_caps.assert_called_once_with(set())

def test_schedule_migration_one_group(complex_round, simple_migration):
    complex_round._schedule_for_controllers = MagicMock(side_effect=None)
    complex_round._reduce_qos_caps = MagicMock(side_effect=None)
    complex_round.schedule_migration(simple_migration, True)
    assert complex_round._migrations == {'s3'}
    simple_migration.get_groups.assert_called_once()
    simple_migration.get_switch.assert_called_once()
    complex_round._schedule_for_controllers.assert_called_once_with(
        simple_migration, True)
    complex_round._reduce_qos_caps.assert_called_once_with({'g0'})

def test_schedule_migration_with_multi_groups(complex_round,
                                              complex_migration):
    complex_round._schedule_for_controllers = MagicMock(side_effect=None)
    complex_round._reduce_qos_caps = MagicMock(side_effect=None)
    complex_round.schedule_migration(complex_migration, True)
    assert complex_round._migrations == {'s1'}
    complex_migration.get_groups.assert_called_once()
    complex_migration.get_switch.assert_called_once()
    complex_round._schedule_for_controllers.assert_called_once_with(
        complex_migration, True)
    complex_round._reduce_qos_caps.assert_called_once_with({'g0', 'g1', 'g2'})

def test_print_migrations_no_migrations(empty_round):
    capturedOutput = io.StringIO()
    sys.stdout = capturedOutput
    empty_round.print_migrations()
    sys.stdout = sys.__stdout__
    assert (capturedOutput.getvalue() ==
            "No migrations scheduled in round 0.\n")

def test_print_migrations_one_migration(simple_round):
    simple_round._migrations = {'s0'}
    capturedOutput = io.StringIO()
    sys.stdout = capturedOutput
    simple_round.print_migrations()
    sys.stdout = sys.__stdout__
    assert (capturedOutput.getvalue() ==
            "Migrations completed in round 1: s0.\n")

def test_print_migrations_multiple_migrations(complex_round):
    complex_round._migrations = {'s3', 's5'}
    capturedOutput = io.StringIO()
    sys.stdout = capturedOutput
    complex_round.print_migrations()
    sys.stdout = sys.__stdout__
    first_part = "Migrations completed in round 0: "
    second_part1 = "s3 s5.\n"
    second_part2 = "s5 s3.\n"
    assert capturedOutput.getvalue() in [first_part + second_part1,
                                         first_part + second_part2]
