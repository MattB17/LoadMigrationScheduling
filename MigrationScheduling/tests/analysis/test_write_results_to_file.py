from unittest.mock import patch, mock_open
from MigrationScheduling.analysis import write_results_to_file


HEADER_STR = "MigrationScheduling.analysis.utils.get_results_header"


@patch(HEADER_STR, return_value="header1\n")
def test_with_no_results(mock_header):
    with patch("builtins.open", mock_open()) as mock_file:
        write_results_to_file([], "output_file.txt", True)
    mock_file.assert_called_once_with("output_file.txt", "w")
    mock_header.assert_called_once_with(True)
    mock_file.return_value.__enter__().write.assert_called_once_with(
        "header1\n")
    mock_file.return_value.__enter__().writelines.assert_called_once_with([])


@patch(HEADER_STR, return_value="header2\n")
def test_with_1_result(mock_header):
    results = ["results0\n"]
    with patch("builtins.open", mock_open()) as mock_file:
        write_results_to_file(results, "/a/dir/results.csv", False)
    mock_file.assert_called_once_with("/a/dir/results.csv", "w")
    mock_header.assert_called_once_with(False)
    mock_file.return_value.__enter__().write.assert_called_once_with(
        "header2\n")
    mock_file.return_value.__enter__().writelines.assert_called_once_with(
        results)


@patch(HEADER_STR, return_value="header3\n")
def test_with_multiple_results(mock_header):
    results = ["results0\n", "results1\n", "results2\n"]
    with patch("builtins.open", mock_open()) as mock_file:
        write_results_to_file(results, "/another/dir/output.dat", True)
    mock_file.assert_called_once_with("/another/dir/output.dat", "w")
    mock_header.assert_called_once_with(True)
    mock_file.return_value.__enter__().write.assert_called_once_with(
        "header3\n")
    mock_file.return_value.__enter__().writelines.assert_called_once_with(
        results)
