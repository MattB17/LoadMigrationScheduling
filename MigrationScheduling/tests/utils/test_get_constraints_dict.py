from unittest.mock import patch, MagicMock
from MigrationScheduling.utils import get_constraints_dict


CONTROL_STR = "MigrationScheduling.utils.get_controller_constraint_dicts"
QOS_STR = "MigrationScheduling.utils.get_qos_constraint_dicts"


@patch(QOS_STR)
@patch(CONTROL_STR)
def test_simple_instance(mock_control_dicts, mock_qos_dicts):
    mock_data = MagicMock()
    mock_data.get_qos_consts = MagicMock(return_value=set())
    control_const = MagicMock()
    mock_control_dicts.return_value = {'c0': control_const}
    mock_qos_dicts.return_value = {}
    assert get_constraints_dict(mock_data, False) == {'c0': control_const}
    mock_control_dicts.assert_called_once_with(mock_data, False)
    mock_data.get_qos_consts.assert_called_once()
    mock_qos_dicts.assert_called_once_with(set())


@patch(QOS_STR)
@patch(CONTROL_STR)
def test_complex_instance(mock_control_dicts, mock_qos_dicts):
    mock_data = MagicMock()
    control_consts = [MagicMock() for _ in range(3)]
    qos_consts = [MagicMock() for _ in range(4)]
    mock_data.get_qos_consts = MagicMock(return_value=set(qos_consts))
    mock_control_dicts.return_value = {'c1': control_consts[0],
                                       'c5': control_consts[1],
                                       'c7': control_consts[2]}
    mock_qos_dicts.return_value = {'g0': qos_consts[0],
                                   'g1': qos_consts[1],
                                   'g2': qos_consts[2],
                                   'g3': qos_consts[3]}
    assert get_constraints_dict(mock_data, True) == {'c1': control_consts[0],
                                                     'c5': control_consts[1],
                                                     'c7': control_consts[2],
                                                     'g0': qos_consts[0],
                                                     'g1': qos_consts[1],
                                                     'g2': qos_consts[2],
                                                     'g3': qos_consts[3]}
    mock_control_dicts.assert_called_once_with(mock_data, True)
    mock_data.get_qos_consts.assert_called_once()
    mock_qos_dicts.assert_called_once_with(set(qos_consts))
