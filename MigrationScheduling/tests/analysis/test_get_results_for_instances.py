from unittest.mock import call, patch, MagicMock
from MigrationScheduling.analysis import get_results_for_instances


EXTRACT_STR = "MigrationScheduling.analysis.utils.extract_file_idx"
BUILD_STR = "MigrationScheduling.analysis.build_results_string"


@patch(BUILD_STR)
@patch(EXTRACT_STR)
def test_with_no_files(mock_extract, mock_build):
    results = ["result0.\n", "result1.\n", "results2.\n"]
    get_results_for_instances(results, [], "migrations", "/empty/dir", False)
    assert results == ["result0.\n", "result1.\n", "results2.\n"]
    mock_extract.assert_not_called()
    mock_build.assert_not_called()


@patch(BUILD_STR, return_value="result7.\n")
@patch(EXTRACT_STR, return_value=7)
def test_with_1_file(mock_extract, mock_build):
    results = ["result5.\n"]
    get_results_for_instances(
        results, ["file7.txt"], "file", "/random/dir", True)
    assert results == ["result5.\n", "result7.\n"]
    mock_extract.assert_called_once_with("file7.txt", "file")
    mock_build.assert_called_once_with(
        "/random/dir", "file7.txt", 7, False, True)


@patch(BUILD_STR, side_effect=("result3.\n", "result4.\n", "result5.\n"))
@patch(EXTRACT_STR, side_effect=(3, 4, 5))
def test_with_multi_file(mock_extract, mock_build):
    results = []
    get_results_for_instances(
        results, ["migrations3.txt", "migrations4.csv", "migrations5.dat"],
        "migrations", "/yet/another/dir", False)
    assert results == ["result3.\n", "result4.\n", "result5.\n"]
    extract_calls = [call("migrations3.txt", "migrations"),
                     call("migrations4.csv", "migrations"),
                     call("migrations5.dat", "migrations")]
    assert mock_extract.call_count == 3
    mock_extract.assert_has_calls(extract_calls)
    build_calls = [
        call("/yet/another/dir", "migrations3.txt", 3, False, False),
        call("/yet/another/dir", "migrations4.csv", 4, False, False),
        call("/yet/another/dir", "migrations5.dat", 5, False, False)
    ]
    assert mock_build.call_count == 3
    mock_build.assert_has_calls(build_calls)
