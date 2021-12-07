import pytest
from unittest.mock import MagicMock
from MigrationScheduling.analysis import get_instances_for_core


@pytest.fixture(scope="function")
def mock_instances():
    return [MagicMock() for _ in range(50)]


def test_at_beginning(mock_instances):
    assert get_instances_for_core(mock_instances, 5, 0) == mock_instances[:5]


def test_in_middle(mock_instances):
    assert get_instances_for_core(
        mock_instances, 10, 2) == mock_instances[20:30]


def test_at_end(mock_instances):
    assert get_instances_for_core(mock_instances, 9, 5) == mock_instances[45:]
