from unittest.mock import call, patch, MagicMock
from MigrationScheduling.algorithms import remove_migration_from_constraints


CONTROL_STR = "MigrationScheduling.algorithms.remove_migration_from_controller"
GROUP_STR = "MigrationScheduling.algorithms.remove_migration_from_group"


@patch(GROUP_STR)
@patch(CONTROL_STR)
def test_with_no_groups(mock_control_remove, mock_group_remove):
    mock_consts0 = MagicMock()
    mock_consts1 = MagicMock()
    mock_control_remove.return_value = mock_consts1
    migration = MagicMock()
    migration.get_src_controller = MagicMock(return_value='c3')
    migration.get_dst_controller = MagicMock(return_value='c0')
    migration.get_groups = MagicMock(return_value=set())
    assert remove_migration_from_constraints(
        migration, mock_consts0, False) == mock_consts1
    migration.get_src_controller.assert_not_called()
    migration.get_dst_controller.assert_called_once()
    mock_control_remove.assert_called_once_with(migration, 'c0', mock_consts0)
    mock_group_remove.assert_not_called()
    migration.get_groups.assert_called_once()


@patch(GROUP_STR)
@patch(CONTROL_STR)
def test_with_one_group(mock_control_remove, mock_group_remove):
    mock_consts0 = MagicMock()
    mock_consts1 = MagicMock()
    migration = MagicMock()
    mock_control_remove.side_effect = (mock_consts0, mock_consts1)
    mock_group_remove.return_value = mock_consts1
    migration.get_src_controller = MagicMock(return_value='c5')
    migration.get_dst_controller = MagicMock(return_value='c1')
    migration.get_groups = MagicMock(return_value={'g2'})
    assert remove_migration_from_constraints(
        migration, mock_consts0, True) == mock_consts1
    control_calls = [call(migration, 'c1', mock_consts0),
                     call(migration, 'c5', mock_consts0)]
    assert mock_control_remove.call_count == 2
    mock_control_remove.assert_has_calls(control_calls)
    mock_group_remove.assert_called_once_with(migration, 'g2', mock_consts1)
    migration.get_src_controller.assert_called_once()
    migration.get_dst_controller.assert_called_once()
    migration.get_groups.assert_called_once()

@patch(GROUP_STR)
@patch(CONTROL_STR)
def test_with_multi_group(mock_control_remove, mock_group_remove):
    mock_consts = [MagicMock() for _ in range(3)]
    migration = MagicMock()
    migration.get_src_controller = MagicMock(return_value='c3')
    migration.get_dst_controller = MagicMock(return_value='c1')
    migration.get_groups = MagicMock(return_value=['g0', 'g1', 'g5'])
    mock_control_remove.side_effect = (mock_consts[0], mock_consts[0])
    mock_group_remove.side_effect = (
        mock_consts[1], mock_consts[2], mock_consts[2])
    assert remove_migration_from_constraints(
        migration, mock_consts[0], True) == mock_consts[2]
    control_calls = [call(migration, 'c1', mock_consts[0]),
                     call(migration, 'c3', mock_consts[0])]
    assert mock_control_remove.call_count == 2
    mock_control_remove.assert_has_calls(control_calls)
    group_calls = [call(migration, 'g0', mock_consts[0]),
                   call(migration, 'g1', mock_consts[1]),
                   call(migration, 'g5', mock_consts[2])]
    assert mock_group_remove.call_count == 3
    mock_group_remove.assert_has_calls(group_calls)
    migration.get_src_controller.assert_called_once()
    migration.get_dst_controller.assert_called_once()
    migration.get_groups.assert_called_once()
