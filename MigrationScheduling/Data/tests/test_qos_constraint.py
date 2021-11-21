import pytest
from unittest.mock import patch, MagicMock
from MigrationScheduling.Data import QosConstraint
from MigrationScheduling import exceptions as exc


VAL_STR = "MigrationScheduling.validation.validate_name"


@pytest.fixture(scope="function")
def qos_const():
    with patch(VAL_STR, side_effect=None) as mock_val:
        qos_const = QosConstraint('g4', 3)
    mock_val.assert_called_once_with('g4', 'g', "QoS Group")
    return qos_const


def test_instantiation(qos_const):
    assert qos_const.get_group() == 'g4'
    assert qos_const.get_group_idx() == 4
    assert qos_const.get_cap() == 3
    assert qos_const.get_switches() == set()


@patch(VAL_STR, side_effect=exc.InvalidName(""))
def test_invalid_name(mock_validate):
    with pytest.raises(exc.InvalidName):
        QosConstraint("q7", 1)

def test_adding_switches(qos_const):
    qos_const.add_switch("s3")
    qos_const.add_switch("s5")
    qos_const.add_switch("s9")
    assert qos_const.get_switches() == {"s3", "s5", "s9"}


def test_str_no_switches(qos_const):
    assert qos_const.__str__() == ("QoS Group g4 allowing 3 "
                                   "concurrent migrations.\n")


def test_str_with_switches(qos_const):
    qos_const._switches = {'s3', 's5'}
    first_part = "QoS Group g4 allowing 3 concurrent migrations.\n"
    second_part_1 = "Switches in QoS Group: s3 s5"
    second_part_2 = "Switches in QoS Group: s5 s3"
    assert qos_const.__str__() in [first_part + second_part_1,
                                   first_part + second_part_2]
