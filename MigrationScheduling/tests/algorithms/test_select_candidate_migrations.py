import pytest
from unittest.mock import patch, MagicMock
from MigrationScheduling.algorithms import select_candidate_migrations


RANDOM_STR = "MigrationScheduling.algorithms.random.sample"


@pytest.fixture(scope="function")
def const_dict1():
    const_dict = MagicMock()
    const_dict.get_switches = MagicMock(return_value={'s0', 's3', 's7'})
    return const_dict


@pytest.fixture(scope="function")
def const_dict2():
    const_dict = MagicMock()
    const_dict.get_switches = MagicMock(return_value={'s1', 's2', 's5', 's6'})
    return const_dict


@patch(RANDOM_STR)
def test_sample_all_directly_specified(mock_random, const_dict1):
    assert select_candidate_migrations(const_dict1, -1) == {'s0', 's3', 's7'}
    const_dict1.get_switches.assert_called_once()
    mock_random.assert_not_called()


@patch(RANDOM_STR)
def test_sample_all_indirectly_specified(mock_random, const_dict2):
    assert select_candidate_migrations(
        const_dict2, 4) == {'s1', 's2', 's5', 's6'}
    assert const_dict2.get_switches.call_count == 2
    mock_random.assert_not_called()


@patch(RANDOM_STR, return_value=['s0', 's7'])
def test_sample_2(mock_random, const_dict1):
    assert select_candidate_migrations(const_dict1, 2) == ['s0', 's7']
    assert const_dict1.get_switches.call_count == 2
    mock_random.assert_called_once_with({'s0', 's3', 's7'}, 2)


@patch(RANDOM_STR, return_value=['s5'])
def test_sample_1(mock_random, const_dict2):
    assert select_candidate_migrations(const_dict2, 1) == ['s5']
    assert const_dict2.get_switches.call_count == 2
    mock_random.assert_called_once_with({'s1', 's2', 's5', 's6'}, 1)
