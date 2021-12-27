import pytest
from unittest.mock import MagicMock, patch
from MigrationScheduling.analysis import simulate_instance


OS_STR = "MigrationScheduling.analysis.os.path.join"


@pytest.fixture(scope="function")
def mock_simulator():
    simulator = MagicMock()
    simulator.run = MagicMock(side_effect=None)
    return simulator


@patch(OS_STR, return_value="/a/dir/migrations0.txt")
def test_with_no_arguments(mock_os, mock_simulator):
    mock_class = MagicMock()
    mock_class.return_value = mock_simulator
    simulate_instance(mock_class, {}, 0, 10, "/a/dir")
    mock_os.assert_called_once_with("/a/dir", "migrations0.txt")
    mock_class.assert_called_once()
    mock_simulator.run.assert_called_once_with(10, "/a/dir/migrations0.txt")


@patch(OS_STR, return_value="/another/dir/migrations3.txt")
def test_with_one_argument(mock_os, mock_simulator):
    mock_class = MagicMock()
    mock_class.return_value = mock_simulator
    simulate_instance(
        mock_class, {'bottleneck_type': 'low'}, 3, 100, "/another/dir")
    mock_os.assert_called_once_with("/another/dir", "migrations3.txt")
    mock_class.assert_called_once_with(bottleneck_type='low')
    mock_simulator.run.assert_called_once_with(
        100, "/another/dir/migrations3.txt")


@patch(OS_STR, return_value="/random/dir/migrations13.txt")
def test_with_multi_arguments(mock_os, mock_simulator):
    mock_class = MagicMock()
    mock_class.return_value = mock_simulator
    simulate_instance(
        mock_class, {'mu': -1.0, 'sigma': 1.0}, 13, 500, "/random/dir")
    mock_os.assert_called_once_with("/random/dir", "migrations13.txt")
    mock_class.assert_called_once_with(mu=-1.0, sigma=1.0)
    mock_simulator.run.assert_called_once_with(
        500, "/random/dir/migrations13.txt")
