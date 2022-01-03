from unittest.mock import call, MagicMock, patch
from MigrationScheduling.analysis import (create_simulated_instances,
                                          simulate_all_instances)


CORE_STR = "MigrationScheduling.analysis.get_cores_and_instances_per_core"
SIM_STR = "MigrationScheduling.analysis.get_sim_tuples_for_core"
PROCESS_STR = "MigrationScheduling.analysis.mp.Process"
INIT_STR = "MigrationScheduling.analysis.initialize_and_join_processes"


@patch(INIT_STR, side_effect=None)
@patch(PROCESS_STR)
@patch(SIM_STR)
@patch(CORE_STR, return_value=(0, 0))
def test_with_no_instances(mock_cores, mock_sim, mock_process, mock_init):
    sim_obj = MagicMock()
    create_simulated_instances(sim_obj, {}, [], 0, "/some/random/dir")
    mock_cores.assert_called_once_with(0)
    mock_sim.assert_not_called()
    mock_process.assert_not_called()
    mock_init.assert_called_once_with([])


@patch(INIT_STR, side_effect=None)
@patch(PROCESS_STR)
@patch(SIM_STR)
@patch(CORE_STR, return_value=(1, 3))
def test_with_one_process(mock_cores, mock_sim, mock_process, mock_init):
    sim_obj = MagicMock()
    process0 = MagicMock()
    out_dir = "/an/output/dir"
    instance_size_lst = [20, 50, 130]
    sim_tups = [(3, 20), (4, 50), (5, 130)]
    mock_sim.return_value = sim_tups
    mock_process.return_value = process0
    args_dict = {'bottleneck_type': 'low'}
    create_simulated_instances(
        sim_obj, args_dict, instance_size_lst, 3, out_dir)
    mock_cores.assert_called_once_with(3)
    mock_sim.assert_called_once_with(instance_size_lst, 3, 0, 3)
    mock_process.assert_called_once_with(
        target=simulate_all_instances,
        args=(sim_obj, args_dict, sim_tups, out_dir))
    mock_init.assert_called_once_with([process0])


@patch(INIT_STR, side_effect=None)
@patch(PROCESS_STR)
@patch(SIM_STR)
@patch(CORE_STR, return_value=(3, 4))
def test_with_multi_processes(mock_cores, mock_sim, mock_process, mock_init):
    sim_obj = MagicMock()
    processes = (MagicMock(), MagicMock(), MagicMock())
    out_dir = "/another/output/dir"
    instance_size_lst = [10, 45, 76, 43, 111, 25, 200, 145, 38, 176]
    sim_tups_lists = [[(5, 10), (6, 45), (7, 76), (8, 43)],
                      [(9, 111), (10, 25), (11, 200), (12, 145)],
                      [(13, 38), (14, 176)]]
    mock_process.side_effect = processes
    mock_sim.side_effect = (
        sim_tups_lists[0], sim_tups_lists[1], sim_tups_lists[2])
    args_dict = {'mu': -1.0, 'sigma': 1.0}
    create_simulated_instances(
        sim_obj, args_dict, instance_size_lst, 5, out_dir)
    mock_cores.assert_called_once_with(10)
    sim_calls = [call(instance_size_lst, 4, i, 5) for i in range(3)]
    assert mock_sim.call_count == 3
    mock_sim.assert_has_calls(sim_calls)
    proc_calls = [call(target=simulate_all_instances,
                       args=(sim_obj, args_dict, sim_tups_lists[i], out_dir))
                  for i in range(3)]
    assert mock_process.call_count == 3
    mock_process.assert_has_calls(proc_calls)
    mock_init.assert_called_once_with(list(processes))
