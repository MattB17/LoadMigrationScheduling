from unittest.mock import call, MagicMock, patch
from MigrationScheduling.analysis import combine_optimal_results_files


OPT_STR = "MigrationScheduling.analysis.utils.get_opt_results_from_file"
WRITE_STR = "MigrationScheduling.analysis.write_results_to_file"


@patch(WRITE_STR, side_effect=None)
@patch(OPT_STR)
def test_with_no_results(mock_opt, mock_write):
    in_dir = "/an/input/dir"
    out_file = "/some/output/file.txt"
    combine_optimal_results_files(in_dir, [], out_file)
    mock_opt.assert_not_called()
    mock_write.assert_called_once_with([], out_file, True)


@patch(WRITE_STR, side_effect=None)
@patch(OPT_STR)
def test_with_one_file(mock_opt, mock_write):
    result_line = "Result line 0\n"
    result_file = "results0.txt"
    in_dir = "/another/input/dir"
    out_file = "/another/output/file.csv"
    mock_opt.return_value = result_line
    combine_optimal_results_files(in_dir, [result_file], out_file)
    mock_opt.assert_called_once_with(in_dir, result_file)
    mock_write.assert_called_once_with([result_line], out_file, True)


@patch(WRITE_STR, side_effect=None)
@patch(OPT_STR)
def test_with_multiple_files(mock_opt, mock_write):
    result_lines = ("Result line 3\n", "", "Result line 5\n")
    result_files = ["results3.txt", "results4.txt", "results5.txt"]
    in_dir = "/some/input/folder"
    out_file = "/some/output/"
    mock_opt.side_effect = result_lines
    combine_optimal_results_files(in_dir, result_files, out_file)
    opt_calls = [call(in_dir, result_files[i]) for i in range(3)]
    assert mock_opt.call_count == 3
    mock_opt.assert_has_calls(opt_calls)
    mock_write.assert_called_once_with(
        [result_lines[0], result_lines[2]], out_file, True)
