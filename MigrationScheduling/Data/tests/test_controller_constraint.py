import pytest
from unittest.mock import patch, MagicMock
from MigrationScheduling.Data import ControllerConstraint
from MigrationScheduling import exceptions as exc


@pytest.fixture(scope="function")
def control_const():
    return ControllerConstraint('c2', 12.5)

@pytest.fixture(scope="function")
def mock_migration():
    migration = MagicMock()
    migration.get_dst_controller = MagicMock(return_value='c2')
    migration.get_load = MagicMock(return_value=6.75)
    return migration



def test_instantiation(control_const):
    assert control_const.get_controller() == 'c2'
    assert control_const.get_controller_idx() == 2
    assert control_const.get_cap() == 12.5
    assert control_const.get_switches() == set()

@patch("MigrationScheduling.validation.validate_name",
       side_effect=exc.InvalidName(""))
def test_invalid_name(mock_validate):
    with pytest.raises(exc.InvalidName):
        ControllerConstraint("c7.5", 5)

def test_adding_switches(control_const):
    control_const.add_switch("s0")
    control_const.add_switch("s3")
    control_const.add_switch("s7")
    assert control_const.get_switches() == {"s0", "s3", "s7"}

def test_get_total_load_no_migrations(control_const):
    assert round(control_const.get_total_load([]), 2) == 0.00

def test_get_total_load_one_migration(control_const, mock_migration):
    assert round(control_const.get_total_load([mock_migration]), 2) == 6.75
    mock_migration.get_dst_controller.assert_called_once()
    mock_migration.get_load.assert_called_once()

def test_get_total_load_multiple_migrations(control_const, mock_migration):
    migrations = [mock_migration] + [MagicMock() for _ in range(2)]
    migrations[1].get_dst_controller = MagicMock(return_value='c3')
    migrations[1].get_load = MagicMock()
    migrations[2].get_dst_controller = MagicMock(return_value='c2')
    migrations[2].get_load = MagicMock(return_value = 3.51)
    assert round(control_const.get_total_load(migrations), 2) == 10.26
    for migration in migrations:
        migration.get_dst_controller.assert_called_once()
    migrations[0].get_load.assert_called_once()
    migrations[1].get_load.assert_not_called()
    migrations[2].get_load.assert_called_once()
