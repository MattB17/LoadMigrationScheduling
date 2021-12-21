from unittest.mock import patch, MagicMock
from MigrationScheduling.analysis import build_optimal_string


TIMER_STR = "MigrationScheduling.analysis.timer"


@patch(TIMER_STR, side_effect=(1.2, 19.7))
def test_with_exception(mock_timer):
    mock_data = MagicMock()
    mock_optimizer = MagicMock()
    mock_optimizer.build_ip_model = MagicMock(side_effect=ValueError(""))
    result_str = build_optimal_string(mock_optimizer, False)
    results = result_str.split(" ")
    assert len(results) == 2
    assert results[0] == "nan"
    assert round(float(results[1]), 1) == 18.5
    mock_optimizer.build_ip_model.assert_called_once_with(
        resiliency=False, verbose=False)
    assert mock_timer.call_count == 2


@patch(TIMER_STR, side_effect=(100.5, 223.1))
def test_without_exception(mock_timer):
    mock_data = MagicMock()
    mock_optimizer = MagicMock()
    mock_optimizer.build_ip_model = MagicMock(return_value=6)
    result_str = build_optimal_string(mock_optimizer, True)
    results = result_str.split(" ")
    assert len(results) == 2
    assert results[0] == "7"
    assert round(float(results[1]), 1) == 122.6
    mock_optimizer.build_ip_model.assert_called_once_with(
        resiliency=True, verbose=False)
    assert mock_timer.call_count == 2
