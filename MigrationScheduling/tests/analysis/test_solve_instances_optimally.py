from unittest.mock import call, patch, MagicMock
from MigrationScheduling.analysis import solve_instances_optimally


EXTRACT_STR = "MigrationScheduling.analysis.utils.extract_file_idx"
WRITE_STR = "MigrationScheduling.analysis.write_optimal_results"


@patch(WRITE_STR)
@patch(EXTRACT_STR)
def test_with_no_instances(mock_extract, mock_write):
    solve_instances_optimally(
        [], "/an/input/dir", "migrations", "/an/output/dir", True)
    mock_extract.assert_not_called()
    mock_write.assert_not_called()


@patch(WRITE_STR, side_effect=None)
@patch(EXTRACT_STR, return_value=5)
def test_with_1_instance(mock_extract, mock_write):
    solve_instances_optimally(
        ["file1.txt"], "/inputs", "file", "/outputs", False)
    mock_extract.assert_called_once_with("file1.txt", "file")
    mock_write.assert_called_once_with(
        "file1.txt", "/inputs", 5, "/outputs", False)


@patch(WRITE_STR, side_effect=None)
@patch(EXTRACT_STR, side_effect=(0, 1, 2))
def test_with_multi_instances(mock_extract, mock_write):
    solve_instances_optimally(
        ["migrations0.txt", "migrations1.csv", "migrations2.dat"],
        "/input/dir", "migrations", "/output/dir", True)
    extract_calls = [call("migrations0.txt", "migrations"),
                     call("migrations1.csv", "migrations"),
                     call("migrations2.dat", "migrations")]
    assert mock_extract.call_count == 3
    mock_extract.assert_has_calls(extract_calls)
    write_calls = [
        call("migrations0.txt", "/input/dir", 0, "/output/dir", True),
        call("migrations1.csv", "/input/dir", 1, "/output/dir", True),
        call("migrations2.dat", "/input/dir", 2, "/output/dir", True)
    ]
    assert mock_write.call_count == 3
    mock_write.assert_has_calls(write_calls)
