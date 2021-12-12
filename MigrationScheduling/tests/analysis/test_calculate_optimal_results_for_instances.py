from unittest.mock import call, MagicMock, patch
from MigrationScheduling.analysis import (
    calculate_optimal_results_for_instances, solve_instances_optimally)


PROCESS_STR = "MigrationScheduling.analysis.mp.Process"
CORES_STR = "MigrationScheduling.analysis.get_cores_and_instances_per_core"
INSTANCES_STR = "MigrationScheduling.analysis.get_instances_for_core"
INIT_STR = "MigrationScheduling.analysis.initialize_and_join_processes"


@patch(INIT_STR, side_effect=None)
@patch(PROCESS_STR)
@patch(INSTANCES_STR)
@patch(CORES_STR, return_value=(0, 0))
def test_with_no_files(mock_cores, mock_instances, mock_process, mock_init):
    calculate_optimal_results_for_instances(
        "/some/dir", "migrations", [], "/another/dir")
    mock_cores.assert_called_once_with(0)
    mock_instances.assert_not_called()
    mock_process.assert_not_called()
    mock_init.assert_called_once_with([])


@patch(INIT_STR, side_effect=None)
@patch(PROCESS_STR)
@patch(INSTANCES_STR)
@patch(CORES_STR, return_value=(1, 1))
def test_with_one_core(mock_cores, mock_instances, mock_process, mock_init):
    mock_instances.return_value = ["instance0.txt"]
    process = MagicMock()
    mock_process.return_value = process
    calculate_optimal_results_for_instances(
        "/an/input/dir", "instance", ["instance0.txt"], "/output/dir")
    mock_cores.assert_called_once_with(1)
    mock_instances.assert_called_once_with(["instance0.txt"], 1, 0)
    mock_process.assert_called_once_with(
        target=solve_instances_optimally,
        args=(["instance0.txt"], "/an/input/dir", "instance", "/output/dir"))
    mock_init.assert_called_once_with([process])


@patch(INIT_STR, side_effect=None)
@patch(PROCESS_STR)
@patch(INSTANCES_STR)
@patch(CORES_STR, return_value=(3, 5))
def test_with_multi_core(mock_cores, mock_instances, mock_process, mock_init):
    files = ["migration{}.txt".format(idx) for idx in range(15)]
    mock_instances.side_effect = (files[:5], files[5:10], files[10:])
    processes = (MagicMock(), MagicMock(), MagicMock())
    mock_process.side_effect = processes
    calculate_optimal_results_for_instances(
        "/a/third/dir", "migration", files, "/a/random/dir")
    mock_cores.assert_called_once_with(15)
    instance_calls = [call(files, 5, idx) for idx in range(3)]
    assert mock_instances.call_count == 3
    mock_instances.assert_has_calls(instance_calls)
    process_calls = [call(target=solve_instances_optimally,
                          args=(files[(5*idx):(5*(idx+1))], "/a/third/dir",
                                "migration", "/a/random/dir"))
                     for idx in range(3)]
    assert mock_process.call_count == 3
    mock_process.assert_has_calls(process_calls)
    mock_init.assert_called_once_with(list(processes))
