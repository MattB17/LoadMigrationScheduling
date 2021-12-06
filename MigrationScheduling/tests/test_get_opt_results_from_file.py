from unittest.mock import patch, mock_open
from MigrationScheduling.utils import get_opt_results_from_file


JOIN_STR = "MigrationScheduling.utils.os.path.join"


@patch(JOIN_STR, return_value="/a/file/path/results.txt")
def test_with_no_data(mock_join):
    mock_read = mock_open(read_data="")
    with patch('builtins.open', mock_read) as reader:
        assert get_opt_results_from_file("/a/file/path", "results.txt") == ""
        reader.assert_called_once_with("/a/file/path/results.txt", "r")


@patch(JOIN_STR, return_value="/file/path/data.rst")
def test_with_insufficient_data(mock_join):
    mock_read = mock_open(read_data="a single line.\n")
    with patch('builtins.open', mock_read) as reader:
        assert get_opt_results_from_file("/file/path", "data.rst") == ""
        reader.assert_called_once_with("/file/path/data.rst", "r")


@patch(JOIN_STR, return_value="/a/dir/output.xls")
def test_with_two_lines(mock_join):
    mock_read = mock_open(read_data="line 1.\nline 2.\n")
    with patch('builtins.open', mock_read) as reader:
        assert get_opt_results_from_file(
            "/a/dir", "output.xls") == "line 2.\n"
        reader.assert_called_once_with("/a/dir/output.xls", "r")


@patch(JOIN_STR, return_value="/file/path/data.rst")
def test_with_multi_lines(mock_join):
    mock_read = mock_open(read_data="header.\nresult0.\nresult1.\nresult2.\n")
    with patch('builtins.open', mock_read) as reader:
        assert get_opt_results_from_file(
            "/some/other/dir", "file.csv") == "result0.\n"
        reader.assert_called_once_with("/file/path/data.rst", "r")
