from unittest.mock import patch
from MigrationScheduling.utils import gaussian_controller_capacity


NORMAL_STR = "MigrationScheduling.utils.np.random.normal"


@patch(NORMAL_STR)
def test_with_high_bottleneck(mock_normal):
    assert gaussian_controller_capacity(1.3, 3.5, "high") == 1.3
    mock_normal.assert_not_called()


@patch(NORMAL_STR, return_value=0.34)
def test_with_medium_bottleneck(mock_normal):
    assert round(
        gaussian_controller_capacity(1.7, 10.7, "medium"), 2) == 4.76
    mock_normal.assert_called_once_with(0.2, 0.3)


@patch(NORMAL_STR, return_value=0.45)
def test_with_low_bottleneck(mock_normal):
    assert round(gaussian_controller_capacity(4.0, 6.0, "low"), 1) == 4.9
    mock_normal.assert_called_once_with(0.5, 0.3)


@patch(NORMAL_STR, return_value=-0.1)
def test_result_too_low(mock_normal):
    assert round(gaussian_controller_capacity(3.8, 9.7, "medium"), 1) == 3.8
    mock_normal.assert_called_once_with(0.2, 0.3)


@patch(NORMAL_STR, return_value=1.2)
def test_result_too_high(mock_normal):
    assert round(gaussian_controller_capacity(2.1, 8.6, "low"), 1) == 8.6
    mock_normal.assert_called_once_with(0.5, 0.3)
