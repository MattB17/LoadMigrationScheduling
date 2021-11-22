from unittest.mock import patch, MagicMock
from MigrationScheduling.utils import get_constraint_dict_for_controller


CONST_STR = "MigrationScheduling.utils.ConstraintDict"
LOAD_STR = "MigrationScheduling.utils.calculate_load_on_controller"


@patch(LOAD_STR, return_value=0.0)
@patch(CONST_STR)
def test_with_no_migrations(mock_const, mock_load):
    const_dict = MagicMock()
    mock_const.return_value = const_dict
    control_const = MagicMock()
    switch_set = {'s0', 's3', 's5'}
    control_const.get_cap = MagicMock(return_value=2.34)
    control_const.get_controller = MagicMock(return_value='c2')
    control_const.get_switches = MagicMock(return_value=switch_set)
    assert get_constraint_dict_for_controller(control_const, []) == const_dict
    mock_load.assert_called_once_with('c2', [])
    mock_const.assert_called_once_with(2.34, 0.0, switch_set)
    control_const.get_cap.assert_called_once()
    control_const.get_controller.assert_called_once()
    control_const.get_switches.assert_called_once()


@patch(LOAD_STR, return_value=11.75)
@patch(CONST_STR)
def test_with_migrations(mock_const, mock_load):
    const_dict = MagicMock()
    mock_const.return_value = const_dict
    control_const = MagicMock()
    migrations = [MagicMock() for _ in range(9)]
    switch_set = {'s1', 's2', 's3', 's7', 's9', 's15', 's21'}
    control_const.get_cap = MagicMock(return_value=5.16)
    control_const.get_controller = MagicMock(return_value='c0')
    control_const.get_switches = MagicMock(return_value=switch_set)
    assert get_constraint_dict_for_controller(
        control_const, migrations) == const_dict
    mock_load.assert_called_once_with('c0', migrations)
    mock_const.assert_called_once_with(5.16, 11.75, switch_set)
    control_const.get_cap.assert_called_once()
    control_const.get_controller.assert_called_once()
    control_const.get_switches.assert_called_once()
