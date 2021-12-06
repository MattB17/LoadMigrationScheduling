from unittest.mock import patch
from MigrationScheduling.analysis import get_cores_and_instances_per_core


CPU_STR = "MigrationScheduling.analysis.mp.cpu_count"


@patch(CPU_STR, return_value=32)
def test_with_low_instance_count(mock_cpu):
    count, per_count = get_cores_and_instances_per_core(10)
    assert count == 10
    assert per_count == 1
    mock_cpu.assert_called_once()


@patch(CPU_STR, return_value=16)
def test_with_high_instance_count(mock_cpu):
    count, per_count = get_cores_and_instances_per_core(2500)
    assert count == 15
    assert per_count == 167
    mock_cpu.assert_called_once()
