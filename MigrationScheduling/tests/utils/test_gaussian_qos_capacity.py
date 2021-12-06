from unittest.mock import patch
from MigrationScheduling.utils import gaussian_qos_capacity


NORMAL_STR = "MigrationScheduling.utils.np.random.normal"


@patch(NORMAL_STR)
def test_with_high_bottleneck(mock_normal):
    assert gaussian_qos_capacity(5, "high") == 1
    mock_normal.assert_not_called()


@patch(NORMAL_STR, return_value=0.4)
def test_with_medium_bottleneck(mock_normal):
    assert gaussian_qos_capacity(5, "medium") == 2
    mock_normal.assert_called_once_with(0.2, 0.3)


@patch(NORMAL_STR, return_value=0.7)
def test_with_low_bottleneck(mock_normal):
    assert gaussian_qos_capacity(11, "low") == 7
    mock_normal.assert_called_once_with(0.5, 0.3)


@patch(NORMAL_STR, return_value=0.01)
def test_result_too_low(mock_normal):
    assert gaussian_qos_capacity(7, "medium") == 1
    mock_normal.assert_called_once_with(0.2, 0.3)


@patch(NORMAL_STR, return_value=1.2)
def test_result_too_high(mock_normal):
    assert gaussian_qos_capacity(12, "low") == 12
    mock_normal.assert_called_once_with(0.5, 0.3)
