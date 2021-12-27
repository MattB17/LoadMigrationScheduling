from unittest.mock import call, MagicMock, patch
from MigrationScheduling.analysis import simulate_all_instances


SIM_STR = "MigrationScheduling.analysis.simulate_instance"


@patch(SIM_STR, side_effect=None)
def test_with_no_tuples(mock_sim):
    mock_class = MagicMock()
    simulate_all_instances(mock_class, {}, [], "/a/dir")
    mock_sim.assert_not_called()


@patch(SIM_STR, side_effect=None)
def test_with_one_tuple(mock_sim):
    mock_class = MagicMock()
    sim_args = {'bottleneck_type': 'low'}
    out_dir = "/another/dir"
    simulate_all_instances(mock_class, sim_args, [(0, 10)], out_dir)
    mock_sim.assert_called_once_with(mock_class, sim_args, 0, 10, out_dir)


@patch(SIM_STR, side_effect=None)
def test_with_multiple_tuples(mock_sim):
    mock_class = MagicMock()
    sim_args = {'mu': -1.0, 'sigma': 1.0}
    out_dir = "/random/dir"
    simulate_all_instances(
        mock_class, sim_args, [(0, 10), (3, 100), (13, 500)], out_dir)
    sim_calls = [call(mock_class, sim_args, 0, 10, out_dir),
                 call(mock_class, sim_args, 3, 100, out_dir),
                 call(mock_class, sim_args, 13, 500, out_dir)]
    assert mock_sim.call_count == 3
    mock_sim.assert_has_calls(sim_calls)
