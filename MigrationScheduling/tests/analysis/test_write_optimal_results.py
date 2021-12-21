from unittest.mock import call, patch, MagicMock, mock_open
from MigrationScheduling.analysis import write_optimal_results


OS_STR = "MigrationScheduling.analysis.os.path.join"
HEADER_STR = "MigrationScheduling.analysis.utils.get_results_header"
BUILD_STR = "MigrationScheduling.analysis.build_results_string"


@patch(BUILD_STR, return_value="")
@patch(HEADER_STR, return_value="")
@patch(OS_STR, return_value="/an/output/dir/results5.txt")
def test_with_no_data(mock_os, mock_header, mock_build):
    with patch("builtins.open", mock_open()) as mock_file:
        write_optimal_results(
            "migrations5.txt", "/an/input/dir", 5, "/an/output/dir", False)
    mock_os.assert_called_once_with("/an/output/dir", "results5.txt")
    mock_file.assert_called_once_with("/an/output/dir/results5.txt", "w")
    mock_header.assert_called_once_with(True)
    mock_build.assert_called_once_with(
        "/an/input/dir", "migrations5.txt", 5, True, False)
    write_calls = [call(""), call("")]
    assert mock_file.return_value.__enter__().write.call_count == 2
    mock_file.return_value.__enter__().write.assert_has_calls(write_calls)


@patch(BUILD_STR, return_value="results string\n")
@patch(HEADER_STR, return_value="header string\n")
@patch(OS_STR, return_value="/another/dir/results1.txt")
def test_with_data(mock_os, mock_header, mock_build):
    with patch("builtins.open", mock_open()) as mock_file:
        write_optimal_results(
            "data1.csv", "/another/dir", 1, "/another/dir", True)
    mock_os.assert_called_once_with("/another/dir", "results1.txt")
    mock_file.assert_called_once_with("/another/dir/results1.txt", "w")
    mock_header.assert_called_once_with(True)
    mock_build.assert_called_once_with(
        "/another/dir", "data1.csv", 1, True, True)
    write_calls = [call("header string\n"), call("results string\n")]
    assert mock_file.return_value.__enter__().write.call_count == 2
    mock_file.return_value.__enter__().write.assert_has_calls(write_calls)
