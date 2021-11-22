import pytest
from unittest.mock import call, patch, MagicMock
from MigrationScheduling.utils import get_qos_constraint_dicts


QOS_STR = "MigrationScheduling.utils.get_constraint_dict_for_qos_group"


@pytest.fixture(scope="function")
def mock_qos_const():
    qos_const = MagicMock()
    qos_const.get_group = MagicMock(return_value='g1')
    return qos_const


@patch(QOS_STR)
def test_with_no_constraints(mock_qos_dict):
    assert get_qos_constraint_dicts(set()) == {}
    mock_qos_dict.assert_not_called()


@patch(QOS_STR)
def test_with_one_constraint(mock_qos_dict, mock_qos_const):
    const_dict = MagicMock()
    mock_qos_dict.return_value = const_dict
    assert get_qos_constraint_dicts({mock_qos_const}) == {'g1': const_dict}
    mock_qos_const.get_group.assert_called_once()
    mock_qos_dict.assert_called_once_with(mock_qos_const)


@patch(QOS_STR)
def test_with_multi_constraint(mock_qos_dict, mock_qos_const):
    qos_consts = [mock_qos_const, MagicMock(), MagicMock()]
    qos_consts[1].get_group = MagicMock(return_value='g3')
    qos_consts[2].get_group = MagicMock(return_value='g7')
    const_dicts = (MagicMock(), MagicMock(), MagicMock())
    mock_qos_dict.side_effect = const_dicts
    assert get_qos_constraint_dicts(qos_consts) == {
        'g1': const_dicts[0], 'g3': const_dicts[1], 'g7': const_dicts[2]}
    for qos_const in qos_consts:
        qos_const.get_group.assert_called_once()
    qos_calls = [call(qos_const) for qos_const in qos_consts]
    assert mock_qos_dict.call_count == len(qos_calls)
    mock_qos_dict.assert_has_calls(qos_calls)
