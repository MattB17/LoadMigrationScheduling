import pytest
from unittest.mock import MagicMock
from MigrationScheduling.utils import get_controller_cap_dict


@pytest.fixture(scope="function")
def mock_const():
    mock_const = MagicMock()
    mock_const.get_controller = MagicMock(return_value='c0')
    mock_const.get_cap = MagicMock(return_value=3.75)
    return mock_const


def test_with_no_constraints():
    assert get_controller_cap_dict([]) == {}


def test_with_one_constraint(mock_const):
    assert get_controller_cap_dict([mock_const]) == {'c0': 3.75}
    mock_const.get_controller.assert_called_once()
    mock_const.get_cap.assert_called_once()


def test_with_multiple_constraints(mock_const):
    constraints = [mock_const] + [MagicMock(), MagicMock()]
    constraints[1].get_controller = MagicMock(return_value='c1')
    constraints[1].get_cap = MagicMock(return_value=2.36)
    constraints[2].get_controller = MagicMock(return_value='c2')
    constraints[2].get_cap = MagicMock(return_value=11.89)
    assert get_controller_cap_dict(constraints) == {
        'c0': 3.75, 'c1': 2.36, 'c2': 11.89}
    for constraint in constraints:
        constraint.get_controller.assert_called_once()
        constraint.get_cap.assert_called_once()
