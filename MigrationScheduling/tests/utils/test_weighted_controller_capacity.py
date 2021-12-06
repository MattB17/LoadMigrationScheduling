from unittest.mock import patch
from MigrationScheduling.utils import weighted_controller_capacity


UNIFORM_STR = "MigrationScheduling.utils.random.uniform"
RANDOM_STR = "MigrationScheduling.utils.np.random.normal"


@patch(RANDOM_STR)
@patch(UNIFORM_STR, return_value=0.95)
def test_high_prop(mock_uniform, mock_random):
    assert weighted_controller_capacity(3.5, 10.1, 0.6, 0.3) == 3.5
    mock_uniform.assert_called_once_with(0, 1)
    mock_random.assert_not_called()


@patch(RANDOM_STR, return_value=0.3)
@patch(UNIFORM_STR, return_value=0.78)
def test_medium_prop(mock_uniform, mock_random):
    assert round(weighted_controller_capacity(1.8, 6.8, 0.7, 0.2), 1) == 3.3
    mock_uniform.assert_called_once_with(0, 1)
    mock_random.assert_called_once_with(0.2, 0.3)


@patch(RANDOM_STR, return_value=0.7)
@patch(UNIFORM_STR, return_value=0.45)
def test_low_prop(mock_uniform, mock_random):
    assert round(weighted_controller_capacity(2.7, 11.9, 0.5, 0.3), 2) == 9.14
    mock_uniform.assert_called_once_with(0, 1)
    mock_random.assert_called_once_with(0.5, 0.3)


@patch(RANDOM_STR, return_value=-0.2)
@patch(UNIFORM_STR, return_value=0.65)
def test_result_too_low(mock_uniform, mock_random):
    assert weighted_controller_capacity(7.9, 10.1, 0.6, 0.3) == 7.9
    mock_uniform.assert_called_once_with(0, 1)
    mock_random.assert_called_once_with(0.2, 0.3)


@patch(RANDOM_STR, return_value=1.1)
@patch(UNIFORM_STR, return_value=0.75)
def test_result_too_high(mock_uniform, mock_random):
    assert weighted_controller_capacity(1.1, 7.5, 0.75, 0.15) == 7.5
    mock_uniform.assert_called_once_with(0, 1)
    mock_random.assert_called_once_with(0.5, 0.3)
