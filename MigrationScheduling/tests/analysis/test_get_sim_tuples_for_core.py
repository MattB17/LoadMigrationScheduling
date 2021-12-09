import pytest
from MigrationScheduling.analysis import get_sim_tuples_for_core


@pytest.fixture(scope="function")
def mock_sizes():
    return [1, 7, 11, 25, 300, 215, 89, 123, 18, 9]


def test_at_start(mock_sizes):
    sim_tups = get_sim_tuples_for_core(mock_sizes, 3, 0, 5)
    assert sim_tups == [(5, 1), (6, 7), (7, 11)]


def test_in_middle(mock_sizes):
    sim_tups = get_sim_tuples_for_core(mock_sizes, 3, 2, 0)
    assert sim_tups == [(6, 89), (7, 123), (8, 18)]


def test_at_end(mock_sizes):
    sim_tups = get_sim_tuples_for_core(mock_sizes, 4, 2, 3)
    assert sim_tups == [(11, 18), (12, 9)]
