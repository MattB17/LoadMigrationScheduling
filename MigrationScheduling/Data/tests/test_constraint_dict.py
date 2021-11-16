import pytest
from MigrationScheduling.Data import ConstraintDict
from MigrationScheduling import exceptions as exc

SWITCH_SET = {'s0', 's1', 's2'}

@pytest.fixture(scope="function")
def constraint_dict():
    return ConstraintDict(5.0, 11.7, SWITCH_SET)


def test_initialization(constraint_dict):
    assert constraint_dict.get_capacity() == 5.0
    assert constraint_dict.get_load() == 11.7
    assert constraint_dict.get_switches() == SWITCH_SET

def test_remove_switch_when_exists(constraint_dict):
    constraint_dict.remove_switch('s1', 3.0)
    assert round(constraint_dict.get_load(), 1) == 8.7
    assert constraint_dict.get_switches() == {'s0', 's2'}

def test_remove_switch_does_not_exist(constraint_dict):
    with pytest.raises(exc.SwitchNotFound):
        constraint_dict.remove_switch('s4', 1.8)
    assert constraint_dict.get_load() == 11.7
    assert constraint_dict.get_switches() == SWITCH_SET

def test_get_load_factor_high_load(constraint_dict):
    assert round(constraint_dict.get_load_factor(), 2) == 2.34

def test_get_load_factor_small_load():
    constraint_dict = ConstraintDict(5.0, 1.0, SWITCH_SET)
    assert round(constraint_dict.get_load_factor(), 1) == 0.2
