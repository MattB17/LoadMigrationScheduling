from unittest.mock import call, MagicMock, patch
from MigrationScheduling.analysis import (
    calculate_heuristic_results_for_instances, get_results_for_instances)


MANAGER_STR = "MigrationScheduling.analysis.mp.Manager"
PROCESS_STR = "MigrationScheduling.analysis.mp.Process"
CORES_STR = "MigrationScheduling.analysis.get_cores_and_instances_per_core"
INSTANCES_STR = "MigrationScheduling.analysis.get_instances_for_core"
INIT_STR = "MigrationScheduling.analysis.initialize_and_join_processes"
WRITE_STR = "MigrationScheduling.analysis.write_results_to_file"


@patch(WRITE_STR, side_effect=None)
@patch(INIT_STR, side_effect=None)
@patch(PROCESS_STR)
@patch(INSTANCES_STR)
@patch(CORES_STR, return_value=(0, 0))
@patch(MANAGER_STR)
def test_with_no_files(mock_manager, mock_cores, mock_instances,
                       mock_process, mock_init, mock_write):
    manager = MagicMock()
    manager.list = MagicMock(return_value=[])
    mock_manager.return_value = manager
    calculate_heuristic_results_for_instances(
        "/some/dir", "migrations", [], "/another/dir/output.txt", True)
    mock_manager.assert_called_once()
    manager.list.assert_called_once()
    mock_cores.assert_called_once_with(0)
    mock_instances.assert_not_called()
    mock_process.assert_not_called()
    mock_init.assert_called_once_with([])
    mock_write.assert_called_once_with([], "/another/dir/output.txt", False)


@patch(WRITE_STR, side_effect=None)
@patch(INIT_STR, side_effect=None)
@patch(PROCESS_STR)
@patch(INSTANCES_STR)
@patch(CORES_STR, return_value=(1, 1))
@patch(MANAGER_STR)
def test_with_one_core(mock_manager, mock_cores, mock_instances,
                       mock_process, mock_init, mock_write):
    manager = MagicMock()
    mock_results = MagicMock()
    manager.list = MagicMock(return_value=mock_results)
    mock_manager.return_value = manager
    mock_instances.return_value = ["instance0.txt"]
    process = MagicMock()
    mock_process.return_value = process
    with patch('builtins.list', return_value=["results0\n"]) as mock_list:
        calculate_heuristic_results_for_instances(
            "/an/input/dir", "instance", ["instance0.txt"],
            "/output/dir/results.csv", False)
    mock_manager.assert_called_once()
    manager.list.assert_called_once()
    mock_cores.assert_called_once_with(1)
    mock_instances.assert_called_once_with(["instance0.txt"], 1, 0)
    mock_process.assert_called_once_with(
        target=get_results_for_instances,
        args=(mock_results, ["instance0.txt"],
              "instance", "/an/input/dir", False))
    mock_init.assert_called_once_with([process])
    mock_list.assert_called_once_with(mock_results)
    mock_write.assert_called_once_with(
        ["results0\n"], "/output/dir/results.csv", False)


@patch(WRITE_STR, side_effect=None)
@patch(INIT_STR, side_effect=None)
@patch(PROCESS_STR)
@patch(INSTANCES_STR)
@patch(CORES_STR, return_value=(3, 5))
@patch(MANAGER_STR)
def test_with_multi_core(mock_manager, mock_cores, mock_instances,
                         mock_process, mock_init, mock_write):
    manager = MagicMock()
    mock_results = MagicMock()
    manager.list = MagicMock(return_value=mock_results)
    mock_manager.return_value = manager
    files = ["migration{}.txt".format(idx) for idx in range(15)]
    mock_instances.side_effect = (files[:5], files[5:10], files[10:])
    processes = (MagicMock(), MagicMock(), MagicMock())
    mock_process.side_effect = processes
    results_lst = ["results{}\n".format(idx) for idx in range(15)]
    with patch('builtins.list', return_value=results_lst) as mock_list:
        calculate_heuristic_results_for_instances(
            "/a/third/dir", "migration", files,
            "/a/random/dir/results.dat", True)
    mock_manager.assert_called_once()
    manager.list.assert_called_once()
    mock_cores.assert_called_once_with(15)
    instance_calls = [call(files, 5, idx) for idx in range(3)]
    assert mock_instances.call_count == 3
    mock_instances.assert_has_calls(instance_calls)
    process_calls = [call(target=get_results_for_instances,
                          args=(mock_results, files[(5*idx):(5*(idx+1))],
                                "migration", "/a/third/dir", True))
                     for idx in range(3)]
    assert mock_process.call_count == 3
    mock_process.assert_has_calls(process_calls)
    mock_init.assert_called_once_with(list(processes))
    mock_list.assert_called_once_with(mock_results)
    mock_write.assert_called_once_with(
        results_lst, "/a/random/dir/results.dat", False)
