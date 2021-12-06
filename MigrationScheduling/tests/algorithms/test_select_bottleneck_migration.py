import pytest
from unittest.mock import patch, MagicMock
from MigrationScheduling.algorithms import select_bottleneck_migration


CONST_STR = "MigrationScheduling.algorithms.get_bottleneck_constraint"
SELECT_STR = "MigrationScheduling.algorithms.select_candidate_migrations"
BOTTLENECK_STR = "MigrationScheduling.algorithms.get_bottleneck_migration"


@patch(BOTTLENECK_STR)
@patch(SELECT_STR)
@patch(CONST_STR)
def test_with_one_candidate(mock_const, mock_select, mock_bottleneck):
    data = MagicMock()
    const = MagicMock()
    migration = MagicMock()
    consts_dict = {'c0': MagicMock(), 'g0': MagicMock(), 'g3': MagicMock()}
    mock_const.return_value = ('c0', const)
    mock_select.return_value = {'s3'}
    mock_bottleneck.return_value = migration
    assert select_bottleneck_migration(data, 1, consts_dict) == migration
    mock_const.assert_called_once_with(consts_dict)
    mock_select.assert_called_once_with(const, 1)
    mock_bottleneck.assert_called_once_with({'s3'}, 'c0', data, consts_dict)


@patch(BOTTLENECK_STR)
@patch(SELECT_STR)
@patch(CONST_STR)
def test_with_multi_candidates(mock_const, mock_select, mock_bottleneck):
    data = MagicMock()
    const = MagicMock()
    migration = MagicMock()
    consts_dict = {'c1': MagicMock(),
                   'c4': MagicMock(),
                   'c11': MagicMock(),
                   'g0': MagicMock(),
                   'g3': MagicMock(),
                   'g7': MagicMock(),
                   'g15': MagicMock()}
    mock_const.return_value = ('g3', const)
    mock_select.return_value = {'s0', 's2'}
    mock_bottleneck.return_value = migration
    assert select_bottleneck_migration(data, 2, consts_dict) == migration
    mock_const.assert_called_once_with(consts_dict)
    mock_select.assert_called_once_with(const, 2)
    mock_bottleneck.assert_called_once_with(
        {'s0', 's2'}, 'g3', data, consts_dict)
