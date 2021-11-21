import pytest
from unittest.mock import MagicMock
from MigrationScheduling.Data import InstanceData


@pytest.fixture(scope="function")
def no_data():
    return InstanceData({}, set(), set(), [], [], [], [])


@pytest.fixture(scope="function")
def mock_migration1():
    migration = MagicMock()
    migration.get_load = MagicMock(return_value=3.24)
    migration.get_switch_idx = MagicMock(return_value=0)
    return migration


@pytest.fixture(scope="function")
def mock_control_const():
    return MagicMock()


@pytest.fixture(scope="function")
def mock_qos_const():
    return MagicMock()


@pytest.fixture(scope="function")
def mock_migration2():
    migration = MagicMock()
    migration.get_load = MagicMock(return_value=17.89)
    migration.get_switch_idx = MagicMock(return_value=7)
    return migration


@pytest.fixture(scope="function")
def multi_migrations(mock_migration1, mock_migration2):
    return {'s0': mock_migration1,
            's7': mock_migration2,
            's9': MagicMock()}

@pytest.fixture(scope="function")
def control_consts():
    return {MagicMock(), MagicMock()}


@pytest.fixture(scope="function")
def qos_consts():
    return {MagicMock() for _ in range(5)}


@pytest.fixture(scope="function")
def small_instance(mock_migration1, mock_control_const, mock_qos_const):
    return InstanceData({'s0': mock_migration1},
                        {mock_control_const},
                        {mock_qos_const},
                        [0],
                        [0],
                        [5],
                        [3])


@pytest.fixture(scope="function")
def large_instance(multi_migrations, control_consts, qos_consts):
    return InstanceData(multi_migrations,
                        control_consts,
                        qos_consts,
                        [2, 7, 9],
                        [0, 1, 2],
                        [3, 5],
                        [0, 1, 2, 3, 4])


def test_instantiation_no_data(no_data):
    assert no_data.get_migrations() == {}
    assert no_data.get_control_consts() == set()
    assert no_data.get_qos_consts() == set()
    assert no_data.get_switch_ids() == []
    assert no_data.get_round_ids() == []
    assert no_data.get_controller_ids() == []
    assert no_data.get_qos_ids() == []


def test_instantiation_small_instance(small_instance, mock_migration1,
                                      mock_control_const, mock_qos_const):
    assert small_instance.get_migrations() == {'s0': mock_migration1}
    assert small_instance.get_control_consts() == {mock_control_const}
    assert small_instance.get_qos_consts() == {mock_qos_const}
    assert small_instance.get_switch_ids() == [0]
    assert small_instance.get_round_ids() == [0]
    assert small_instance.get_controller_ids() == [5]
    assert small_instance.get_qos_ids() == [3]


def test_instantiation_large_instance(large_instance, multi_migrations,
                                      control_consts, qos_consts):
    assert large_instance.get_migrations() == multi_migrations
    assert large_instance.get_control_consts() == control_consts
    assert large_instance.get_qos_consts() == qos_consts
    assert large_instance.get_switch_ids() == [2, 7, 9]
    assert large_instance.get_round_ids() == [0, 1, 2]
    assert large_instance.get_controller_ids() == [3, 5]
    assert large_instance.get_qos_ids() == [0, 1, 2, 3, 4]


def test_get_migration(small_instance, mock_migration1,
                       large_instance, mock_migration2):
    assert small_instance.get_migration('s0') == mock_migration1
    assert large_instance.get_migration('s7') == mock_migration2


def test_get_load(small_instance, mock_migration1,
                  large_instance, mock_migration2):
    assert small_instance.get_load('s0') == 3.24
    mock_migration1.get_load.assert_called_once()

    assert large_instance.get_load('s7') == 17.89
    mock_migration2.get_load.assert_called_once()


def test_get_switch_id(small_instance, mock_migration1,
                       large_instance, mock_migration2):
    assert small_instance.get_switch_id('s0') == 0
    mock_migration1.get_switch_idx.assert_called_once()

    assert large_instance.get_switch_id('s7') == 7
    mock_migration2.get_switch_idx.assert_called_once()


def test_get_size_string(no_data, small_instance, large_instance):
    assert no_data.get_size_string() == "0 0 0"
    assert small_instance.get_size_string() == "1 1 1"
    assert large_instance.get_size_string() == "3 2 5"
