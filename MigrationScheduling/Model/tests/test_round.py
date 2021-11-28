import pytest
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
