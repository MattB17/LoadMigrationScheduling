import pytest
from unittest.mock import MagicMock
from MigrationScheduling.algorithms import get_bottleneck_constraint


@pytest.fixture(scope="function")
def mock_constraint():
    const = MagicMock()
    const.get_load_factor = MagicMock(return_value=1.7)
    return const


def test_with_no_constraints():
    const_name, const = get_bottleneck_constraint({})
    assert const_name is None
    assert const is None


def test_with_one_constraint(mock_constraint):
    const_name, const = get_bottleneck_constraint({'c0': mock_constraint})
    assert const_name == 'c0'
    assert const == mock_constraint
    mock_constraint.get_load_factor.assert_called_once()


def test_with_multiple_constraints(mock_constraint):
    const_dict = {'c2': mock_constraint,
                  'c5': MagicMock(),
                  'g0': MagicMock(),
                  'g3': MagicMock(),
                  'g9': MagicMock()}
    const_dict['c5'].get_load_factor = MagicMock(return_value=0.8)
    const_dict['g0'].get_load_factor = MagicMock(return_value=1.9)
    const_dict['g3'].get_load_factor = MagicMock(return_value=2.5)
    const_dict['g9'].get_load_factor = MagicMock(return_value=0.5)
    const_name, const = get_bottleneck_constraint(const_dict)
    assert const_name == 'g3'
    assert const == const_dict['g3']
    for const in const_dict.values():
        const.get_load_factor.assert_called_once()
