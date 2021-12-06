import pytest
from unittest.mock import MagicMock
from MigrationScheduling.utils import get_qos_group_cap_dict


@pytest.fixture(scope="function")
def mock_const():
    mock_const = MagicMock()
    mock_const.get_group = MagicMock(return_value='g2')
    mock_const.get_cap = MagicMock(return_value=2)
    return mock_const


def test_with_no_constraints():
    assert get_qos_group_cap_dict([]) == {}


def test_with_one_constraint(mock_const):
    assert get_qos_group_cap_dict([mock_const]) == {'g2': 2}
    mock_const.get_group.assert_called_once()
    mock_const.get_cap.assert_called_once()


def test_with_multiple_constraints(mock_const):
    constraints = [mock_const] + [MagicMock(), MagicMock()]
    constraints[1].get_group = MagicMock(return_value='g3')
    constraints[1].get_cap = MagicMock(return_value=5)
    constraints[2].get_group = MagicMock(return_value='g7')
    constraints[2].get_cap = MagicMock(return_value=1)
    assert get_qos_group_cap_dict(constraints) == {
        'g2': 2, 'g3': 5, 'g7': 1}
    for constraint in constraints:
        constraint.get_group.assert_called_once()
        constraint.get_cap.assert_called_once()
