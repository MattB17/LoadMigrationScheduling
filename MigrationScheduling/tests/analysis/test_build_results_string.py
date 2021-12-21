from unittest.mock import patch, MagicMock
from MigrationScheduling.analysis import build_results_string


OPTIMIZER_STR = "MigrationScheduling.analysis.Optimizer"
HEURISTICS_STR = "MigrationScheduling.analysis.build_heuristics_string"
OPT_STR = "MigrationScheduling.analysis.build_optimal_string"
OS_STR = "MigrationScheduling.analysis.os.path.join"


@patch(OPT_STR)
@patch(HEURISTICS_STR, return_value="6 1.7 6 2.5")
@patch(OS_STR, return_value="/some/instance/file.txt")
@patch(OPTIMIZER_STR)
def test_without_optimizer(mock_optimizer, mock_os,
                           build_heuristics, build_opt):
    optimizer = MagicMock()
    mock_optimizer.return_value = optimizer
    optimizer.get_model_data = MagicMock(side_effect=None)
    mock_data = MagicMock()
    optimizer.instance_data = MagicMock(return_value=mock_data)
    optimizer.get_size_string = MagicMock(return_value="15 10 20")
    result_str = build_results_string(
        "/some/instance", "file.txt", 1, False, True)
    assert result_str == "1 15 10 20 6 1.7 6 2.5\n"
    mock_optimizer.assert_called_once()
    mock_os.assert_called_once_with("/some/instance", "file.txt")
    optimizer.get_model_data.assert_called_once_with(
        "/some/instance/file.txt")
    optimizer.get_size_string.assert_called_once()
    optimizer.instance_data.assert_called_once()
    build_heuristics.assert_called_once_with(mock_data, True)
    build_opt.assert_not_called()


@patch(OPT_STR, return_value="7 132.4")
@patch(HEURISTICS_STR, return_value="8 1.9 7 3.2")
@patch(OS_STR, return_value="/another/instance/results.csv")
@patch(OPTIMIZER_STR)
def test_with_optimizer(mock_optimizer, mock_os, build_heuristics, build_opt):
    optimizer = MagicMock()
    mock_optimizer.return_value = optimizer
    optimizer.get_model_data = MagicMock(side_effect=None)
    mock_data = MagicMock()
    optimizer.instance_data = MagicMock(return_value=mock_data)
    optimizer.get_size_string = MagicMock(return_value="105 40 97")
    result_str = build_results_string(
        "/another/instance", "results.csv", 0, True, False)
    assert result_str == "0 105 40 97 8 1.9 7 3.2 7 132.4\n"
    mock_optimizer.assert_called_once()
    mock_os.assert_called_once_with("/another/instance", "results.csv")
    optimizer.get_model_data.assert_called_once_with(
        "/another/instance/results.csv")
    optimizer.get_size_string.assert_called_once()
    optimizer.instance_data.assert_called_once()
    build_heuristics.assert_called_once_with(mock_data, False)
    build_opt.assert_called_once_with(optimizer, False)
