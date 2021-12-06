import pytest
from unittest.mock import MagicMock
from MigrationScheduling.algorithms import find_scheduling_round


@pytest.fixture(scope="function")
def mock_migration():
    return MagicMock()


@pytest.fixture(scope="function")
def mock_round():
    return MagicMock()


def test_with_no_rounds(mock_migration):
    assert find_scheduling_round([], 0, mock_migration) == 0


def test_with_one_round(mock_migration, mock_round):
    mock_round.can_schedule_migration = MagicMock(return_value=True)
    assert find_scheduling_round([mock_round], 1, mock_migration) == 0
    mock_round.can_schedule_migration.assert_called_once()

def test_with_multi_round_can_fit(mock_migration, mock_round):
    rounds = [mock_round, MagicMock(), MagicMock()]
    mock_round.can_schedule_migration = MagicMock(return_value=False)
    rounds[1].can_schedule_migration = MagicMock(return_value=True)
    rounds[2].can_schedule_migration = MagicMock()
    assert find_scheduling_round(rounds, 3, mock_migration) == 1
    mock_round.can_schedule_migration.assert_called_once()
    rounds[1].can_schedule_migration.assert_called_once()
    rounds[2].can_schedule_migration.assert_not_called()

def test_with_multi_round_cant_fit(mock_migration, mock_round):
    rounds = [mock_round, MagicMock(), MagicMock(), MagicMock()]
    for round in rounds:
        round.can_schedule_migration = MagicMock(return_value=False)
    assert find_scheduling_round(rounds, 4, mock_migration) == 4
    for round in rounds:
        round.can_schedule_migration.assert_called_once()
