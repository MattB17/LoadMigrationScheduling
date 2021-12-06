from unittest.mock import patch
from MigrationScheduling.utils import weighted_qos_capacity


UNIFORM_STR = "MigrationScheduling.utils.random.uniform"
RANDOM_STR = "MigrationScheduling.utils.np.random.normal"


@patch(RANDOM_STR)
@patch(UNIFORM_STR, return_value=0.95)
def test_high_prop(mock_uniform, mock_random):
    assert weighted_qos_capacity(7, 0.6, 0.3) == 1
    mock_uniform.assert_called_once_with(0, 1)
    mock_random.assert_not_called()


@patch(RANDOM_STR, return_value=0.3)
@patch(UNIFORM_STR, return_value=0.78)
def test_medium_prop(mock_uniform, mock_random):
    assert weighted_qos_capacity(10, 0.7, 0.2) == 3
    mock_uniform.assert_called_once_with(0, 1)
    mock_random.assert_called_once_with(0.2, 0.3)


@patch(RANDOM_STR, return_value=0.7)
@patch(UNIFORM_STR, return_value=0.45)
def test_low_prop(mock_uniform, mock_random):
    assert weighted_qos_capacity(11, 0.5, 0.3) == 7
    mock_uniform.assert_called_once_with(0, 1)
    mock_random.assert_called_once_with(0.5, 0.3)


@patch(RANDOM_STR, return_value=-0.2)
@patch(UNIFORM_STR, return_value=0.65)
def test_result_too_low(mock_uniform, mock_random):
    assert weighted_qos_capacity(6, 0.6, 0.2) == 1
    mock_uniform.assert_called_once_with(0, 1)
    mock_random.assert_called_once_with(0.2, 0.3)


@patch(RANDOM_STR, return_value=1.1)
@patch(UNIFORM_STR, return_value=0.75)
def test_result_too_high(mock_uniform, mock_random):
    assert weighted_qos_capacity(12, 0.75, 0.2) == 12
    mock_uniform.assert_called_once_with(0, 1)
    mock_random.assert_called_once_with(0.5, 0.3)
