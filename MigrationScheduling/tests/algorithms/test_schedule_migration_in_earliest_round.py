import pytest
from unittest.mock import patch, MagicMock
from MigrationScheduling.algorithms import schedule_migration_in_earliest_round


ROUND_STR = "MigrationScheduling.algorithms.Round"
FIND_STR = "MigrationScheduling.algorithms.find_scheduling_round"


CONTROLLER_CAPS1 = {'c0': 11.3, 'c1': 12.5, 'c2': 6.8}
QOS_CAPS1 = {'g0': 1, 'g1': 3, 'g2': 7, 'g3': 2}
CONTROLLER_CAPS2 = {'c3': 1.9, 'c5': 12.9, 'c10': 8.9, 'c13': 7.6}
QOS_CAPS2 = {'g1': 1, 'g3': 1, 'g7': 5, 'g11': 3}


@pytest.fixture(scope="function")
def mock_migration():
    return MagicMock()


@patch(FIND_STR, return_value=0)
@patch(ROUND_STR)
def test_with_no_rounds(mock_round, mock_find, mock_migration):
    new_round = MagicMock()
    mock_round.return_value = new_round
    new_round.schedule_migration = MagicMock(side_effect=None)
    result_rounds, result_cnt = schedule_migration_in_earliest_round(
        [], 0, mock_migration, CONTROLLER_CAPS1, QOS_CAPS1)
    mock_find.assert_called_once_with([], 0, mock_migration)
    mock_round.assert_called_once_with(0, CONTROLLER_CAPS1, QOS_CAPS1)
    new_round.schedule_migration.assert_called_once_with(mock_migration)
    assert result_rounds == [new_round]
    assert result_cnt == 1

@patch(FIND_STR, return_value=0)
@patch(ROUND_STR)
def test_with_one_round(mock_round, mock_find, mock_migration):
    round = MagicMock()
    round.schedule_migration = MagicMock(side_effect=None)
    result_rounds, result_cnt = schedule_migration_in_earliest_round(
        [round], 1, mock_migration, CONTROLLER_CAPS1, QOS_CAPS1)
    mock_find.assert_called_once_with([round], 1, mock_migration)
    mock_round.assert_not_called()
    round.schedule_migration.assert_called_once_with(mock_migration)
    assert result_rounds == [round]
    assert result_cnt == 1

@patch(FIND_STR, return_value=1)
@patch(ROUND_STR)
def test_with_multi_round_can_fit(mock_round, mock_find, mock_migration):
    rounds = [MagicMock() for _ in range(3)]
    rounds[1].schedule_migration = MagicMock(side_effect=None)
    result_rounds, result_cnt = schedule_migration_in_earliest_round(
        rounds, 3, mock_migration, CONTROLLER_CAPS2, QOS_CAPS2)
    mock_find.assert_called_once_with(rounds, 3, mock_migration)
    mock_round.assert_not_called()
    rounds[1].schedule_migration.assert_called_once_with(mock_migration)
    assert result_rounds == rounds
    assert result_cnt == 3

@patch(FIND_STR, return_value=5)
@patch(ROUND_STR)
def test_with_multi_round_cant_fit(mock_round, mock_find, mock_migration):
    rounds = [MagicMock() for _ in range(5)]
    new_round = MagicMock()
    mock_round.return_value = new_round
    new_round.schedule_migration = MagicMock(side_effect=None)
    result_rounds, result_cnt = schedule_migration_in_earliest_round(
        rounds, 5, mock_migration, CONTROLLER_CAPS2, QOS_CAPS2)
    mock_find.assert_called_once_with(rounds, 5, mock_migration)
    mock_round.assert_called_once_with(5, CONTROLLER_CAPS2, QOS_CAPS2)
    new_round.schedule_migration.assert_called_once_with(mock_migration)
    assert result_rounds == rounds + [new_round]
    assert result_cnt == 6
