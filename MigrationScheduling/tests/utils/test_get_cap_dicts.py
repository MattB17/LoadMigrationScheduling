from unittest.mock import patch, MagicMock
from MigrationScheduling.utils import get_cap_dicts

CONTROL_CAPS = {'c1': 12.54, 'c2': 3.68, 'c7': 1.08}
QOS_CAPS = {'g0': 3, 'g2': 1, 'g5': 1, 'g6': 5, 'g11': 2}


CONTROLLER_STR = "MigrationScheduling.utils.get_controller_cap_dict"
QOS_STR = "MigrationScheduling.utils.get_qos_group_cap_dict"


@patch(QOS_STR, return_value={})
@patch(CONTROLLER_STR, return_value={})
def test_with_no_constraints(mock_control_caps, mock_qos_caps):
    mock_data = MagicMock()
    mock_data.get_control_consts = MagicMock(return_value=set())
    mock_data.get_qos_consts = MagicMock(return_value=set())
    control_caps, qos_caps = get_cap_dicts(mock_data)
    assert control_caps == {}
    assert qos_caps == {}
    mock_data.get_control_consts.assert_called_once()
    mock_data.get_qos_consts.assert_called_once()
    mock_control_caps.assert_called_once_with(set())
    mock_qos_caps.assert_called_once_with(set())


@patch(QOS_STR, return_value={})
@patch(CONTROLLER_STR, return_value={'c0': 3.24})
def test_with_one_constraint(mock_control_caps, mock_qos_caps):
    mock_data = MagicMock()
    control_consts = {MagicMock()}
    mock_data.get_control_consts = MagicMock(return_value=control_consts)
    mock_data.get_qos_consts = MagicMock(return_value=set())
    control_caps, qos_caps = get_cap_dicts(mock_data)
    assert control_caps == {'c0': 3.24}
    assert qos_caps == {}
    mock_data.get_control_consts.assert_called_once()
    mock_data.get_qos_consts.assert_called_once()
    mock_control_caps.assert_called_once_with(control_consts)
    mock_qos_caps.assert_called_once_with(set())


@patch(QOS_STR, return_value=QOS_CAPS)
@patch(CONTROLLER_STR, return_value=CONTROL_CAPS)
def test_with_multi_constraints(mock_control_caps, mock_qos_caps):
    mock_data = MagicMock()
    control_consts = {MagicMock() for _ in range(3)}
    qos_consts = {MagicMock() for _ in range(5)}
    mock_data.get_control_consts = MagicMock(return_value=control_consts)
    mock_data.get_qos_consts = MagicMock(return_value=qos_consts)
    control_caps, qos_caps = get_cap_dicts(mock_data)
    assert control_caps == CONTROL_CAPS
    assert qos_caps == QOS_CAPS
    mock_data.get_control_consts.assert_called_once()
    mock_data.get_qos_consts.assert_called_once()
    mock_control_caps.assert_called_once_with(control_consts)
    mock_qos_caps.assert_called_once_with(qos_consts)
