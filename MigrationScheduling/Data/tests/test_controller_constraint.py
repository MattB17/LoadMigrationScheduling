import pytest
from unittest.mock import patch, MagicMock
from MigrationScheduling.Data import ControllerConstraint
from MigrationScheduling import exceptions as exc


CONST_STR = "MigrationScheduling.Data.ControllerConstraint.ConstraintDict"


@pytest.fixture(scope="function")
def control_const():
    return ControllerConstraint('c2', 12.5)


def test_instantiation(control_const):
    assert control_const.get_controller() == 'c2'
    assert control_const.get_controller_idx() == 2
    assert control_const.get_cap() == 12.5
    assert control_const.get_switches() == set()

@patch("MigrationScheduling.validation.validate_name",
       side_effect=exc.InvalidName(""))
def test_invalid_name(mock_validate):
    with pytest.raises(exc.InvalidName):
        ControllerConstraint("c7.5", 5)

def test_adding_switches(control_const):
    control_const.add_switch("s0")
    control_const.add_switch("s3")
    control_const.add_switch("s7")
    assert control_const.get_switches() == {"s0", "s3", "s7"}

def test_str_no_switches(control_const):
    assert control_const.__str__() == ("Constraint for controller c2 " +
                                       "with a capacity of 12.50.\n")

def test_str_with_switches(control_const):
    control_const.add_switch("s3")
    control_const.add_switch("s7")
    first_part = "Constraint for controller c2 with a capacity of 12.50.\n"
    second_part_1 = "Destination for switches: s3 s7"
    second_part_2 = "Destination for switches: s7 s3"
    assert control_const.__str__() in [first_part + second_part_1,
                                       first_part + second_part_2]
