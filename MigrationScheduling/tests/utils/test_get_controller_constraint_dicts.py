import pytest
from unittest.mock import call, patch, MagicMock
from MigrationScheduling.utils import get_controller_constraint_dicts


CONTROL_STR = "MigrationScheduling.utils.get_constraint_dict_for_controller"


@pytest.fixture(scope="function")
def mock_control_const():
    control_const = MagicMock()
    control_const.get_controller = MagicMock(return_value='c0')
    return control_const


@patch(CONTROL_STR)
def test_with_no_constraints(mock_const_dict):
    mock_data = MagicMock()
    mock_data.get_migrations = MagicMock(return_value={'s3': MagicMock()})
    mock_data.get_control_consts = MagicMock(return_value=set())
    assert get_controller_constraint_dicts(mock_data, True) == {}
    mock_data.get_migrations.assert_called_once()
    mock_data.get_control_consts.assert_called_once()
    mock_const_dict.assert_not_called()


@patch(CONTROL_STR)
def test_with_one_constraint(mock_const_dict, mock_control_const):
    mock_data = MagicMock()
    migrations = [MagicMock() for _ in range(3)]
    mock_data.get_migrations = MagicMock(return_value={
        's0': migrations[0], 's2': migrations[1], 's5': migrations[2]})
    mock_data.get_control_consts = MagicMock(
        return_value={mock_control_const})
    const_dict = MagicMock()
    mock_const_dict.return_value = const_dict
    assert get_controller_constraint_dicts(
        mock_data, False) == {'c0': const_dict}
    mock_data.get_migrations.assert_called_once()
    mock_data.get_control_consts.assert_called_once()
    mock_const_dict.assert_called_once_with(
        mock_control_const, set(migrations), False)
    mock_control_const.get_controller.assert_called_once()


@patch(CONTROL_STR)
def test_with_multi_constraints(mock_const_dict, mock_control_const):
    mock_data = MagicMock()
    migrations = [MagicMock() for _ in range(3)]
    mock_data.get_migrations = MagicMock(return_value={
        's1': migrations[0], 's9': migrations[1], 's11': migrations[2]})
    control_consts = [mock_control_const, MagicMock(), MagicMock()]
    control_consts[1].get_controller = MagicMock(return_value='c3')
    control_consts[2].get_controller = MagicMock(return_value='c7')
    mock_data.get_control_consts = MagicMock(return_value=control_consts)
    const_dicts = (MagicMock(), MagicMock(), MagicMock())
    mock_const_dict.side_effect = const_dicts
    assert get_controller_constraint_dicts(mock_data, True) == {
        'c0': const_dicts[0], 'c3': const_dicts[1], 'c7': const_dicts[2]}
    mock_data.get_migrations.assert_called_once()
    mock_data.get_control_consts.assert_called_once()
    for control_const in control_consts:
        control_const.get_controller.assert_called_once()
    dict_calls = [call(control_const, set(migrations), True)
                  for control_const in control_consts]
    assert mock_const_dict.call_count == 3
    mock_const_dict.assert_has_calls(dict_calls)
