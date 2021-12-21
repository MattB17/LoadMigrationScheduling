from MigrationScheduling import specs
from unittest.mock import patch, MagicMock
from MigrationScheduling.analysis import build_heuristics_string


TIMER_STR = "MigrationScheduling.analysis.timer"
VFF_STR = "MigrationScheduling.analysis.algorithms.vector_first_fit"
CBF_STR = "MigrationScheduling.analysis.algorithms.current_bottleneck_first"


@patch(CBF_STR, return_value=7)
@patch(VFF_STR, return_value=8)
@patch(TIMER_STR, side_effect=(1.1, 2.3, 5.7, 8.9))
def test_no_resilience(mock_timer, mock_vff, mock_cbf):
    mock_data = MagicMock()
    result_str = build_heuristics_string(mock_data, False)
    results = [float(x) for x in result_str.split(" ")]
    assert len(results) == 4
    assert round(results[0], 0) == 8
    assert round(results[1], 1) == 1.2
    assert round(results[2], 0) == 7
    assert round(results[3], 1) == 3.2
    assert mock_timer.call_count == 4
    mock_vff.assert_called_once_with(mock_data, False)
    mock_cbf.assert_called_once_with(mock_data, specs.CBF_CHOICES, False)


@patch(CBF_STR, return_value=10)
@patch(VFF_STR, return_value=12)
@patch(TIMER_STR, side_effect=(1.3, 2.9, 3.2, 7.8))
def test_with_resilience(mock_timer, mock_vff, mock_cbf):
    mock_data = MagicMock()
    result_str = build_heuristics_string(mock_data, True)
    results = [float(x) for x in result_str.split(" ")]
    assert len(results) == 4
    assert round(results[0], 0) == 12
    assert round(results[1], 1) == 1.6
    assert round(results[2], 0) == 10
    assert round(results[3], 1) == 4.6
    assert mock_timer.call_count == 4
    mock_vff.assert_called_once_with(mock_data, True)
    mock_cbf.assert_called_once_with(mock_data, specs.CBF_CHOICES, True)
