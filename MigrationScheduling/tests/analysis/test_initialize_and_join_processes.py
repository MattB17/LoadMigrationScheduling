from unittest.mock import MagicMock
from MigrationScheduling.analysis import initialize_and_join_processes


def test_empty():
    initialize_and_join_processes([])


def test_non_empty():
    processes = [MagicMock() for _ in range(5)]
    for process in processes:
        process.start = MagicMock()
        process.join = MagicMock()
    initialize_and_join_processes(processes)
    for process in processes:
        process.start.assert_called_once()
        process.join.assert_called_once()
