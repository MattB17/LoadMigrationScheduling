from MigrationScheduling.utils import get_results_header


def test_not_running_optimizer():
    assert get_results_header(False) == (
        "instance_idx num_migrations num_controllers num_groups " +
        "vff vff_time cbf cbf_time\n")


def test_when_running_optimizer():
    assert get_results_header(True) == (
        "instance_idx num_migrations num_controllers num_groups " +
        "vff vff_time cbf cbf_time opt opt_time\n")
