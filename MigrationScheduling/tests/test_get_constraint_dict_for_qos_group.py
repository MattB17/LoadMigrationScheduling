from unittest.mock import patch, MagicMock
from MigrationScheduling.utils import get_constraint_dict_for_qos_group


CONST_STR = "MigrationScheduling.utils.ConstraintDict"


@patch(CONST_STR)
def test_with_one_switch(mock_const):
    const_dict = MagicMock()
    mock_const.return_value = const_dict
    qos_const = MagicMock()
    switch_set = {'s3'}
    qos_const.get_cap = MagicMock(return_value=1)
    qos_const.get_switches = MagicMock(return_value=switch_set)
    assert get_constraint_dict_for_qos_group(qos_const) == const_dict
    mock_const.assert_called_once_with(1, 1, switch_set)
    qos_const.get_cap.assert_called_once()
    qos_const.get_switches.assert_called_once()


@patch(CONST_STR)
def test_with_multiple_switches(mock_const):
    const_dict = MagicMock()
    mock_const.return_value = const_dict
    qos_const = MagicMock()
    switch_set = {'s0', 's2', 's5', 's9', 's11', 's20', 's35'}
    qos_const.get_cap = MagicMock(return_value=3)
    qos_const.get_switches = MagicMock(return_value=switch_set)
    assert get_constraint_dict_for_qos_group(qos_const) == const_dict
    mock_const.assert_called_once_with(3, 7, switch_set)
    qos_const.get_cap.assert_called_once()
    qos_const.get_switches.assert_called_once()
