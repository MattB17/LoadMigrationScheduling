from unittest.mock import call, patch
from MigrationScheduling.utils import get_all_files_by_pattern


OS_STR = "MigrationScheduling.utils.os.listdir"
MATCH_STR = "MigrationScheduling.utils.re.match"


@patch(MATCH_STR)
@patch(OS_STR)
def test_with_no_files(mock_os, mock_match):
    mock_os.return_value = []
    assert get_all_files_by_pattern("/some/directory", "migration") == []
    mock_os.assert_called_once_with("/some/directory")
    mock_match.assert_not_called()


@patch(MATCH_STR)
@patch(OS_STR)
def test_with_one_file(mock_os, mock_match):
    mock_os.return_value = ["migration0.txt"]
    mock_match.return_value = True
    assert get_all_files_by_pattern(
        "/another/directory", "migration") == ["migration0.txt"]
    mock_os.assert_called_once_with("/another/directory")
    mock_match.assert_called_once_with(r"migration.*\.txt", "migration0.txt")


@patch(MATCH_STR)
@patch(OS_STR)
def test_with_multiple_files(mock_os, mock_match):
    files = ["fileA.txt", "ADifferentFile.txt", "fileB.txt", "fileC.csv"]
    mock_os.return_value = files
    mock_match.side_effect = (True, False, True, False)
    assert get_all_files_by_pattern(
        "/a/third/dir", "file") == ["fileA.txt", "fileB.txt"]
    mock_os.assert_called_once_with("/a/third/dir")
    match_calls = [call(r"file.*\.txt", file_name) for file_name in files]
    assert mock_match.call_count == len(files)
    mock_match.assert_has_calls(match_calls)
