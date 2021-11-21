import pytest
from unittest.mock import MagicMock
from MigrationScheduling.Data import InstanceData


@pytest.fixture(scope="function")
def no_data():
    return InstanceData({}, set(), set(), [], [], [], [])


@pytest.fixture(scope="function")
def mock_migration():
    return MagicMock()


@pytest.fixture(scope="function")
def mock_control_const():
    return MagicMock()


@pytest.fixture(scope="function")
def mock_qos_const():
    return MagicMock()


@pytest.fixture(scope="function")
def small_instance(mock_migration, mock_control_const, mock_qos_const):
    return InstanceData({'s0': mock_migration},
                        {mock_control_const},
                        {mock_qos_const},
                        [0],
                        [0],
                        [5],
                        [3])


def test_instantiation_no_data(no_data):
    assert no_data.get_migrations() == {}
    assert no_data.get_control_consts() == set()
    assert no_data.get_qos_consts() == set()
    assert no_data.get_switch_ids() == []
    assert no_data.get_round_ids() == []
    assert no_data.get_controller_ids() == []
    assert no_data.get_qos_ids() == []


def test_instantiation_small_instance(small_instance, mock_migration,
                                      mock_control_const, mock_qos_const):
    assert small_instance.get_migrations() == {'s0': mock_migration}
    assert small_instance.get_control_consts() == {mock_control_const}
    assert small_instance.get_qos_consts() == {mock_qos_const}
    assert small_instance.get_switch_ids() == [0]
    assert small_instance.get_round_ids() == [0]
    assert small_instance.get_controller_ids() == [5]
    assert small_instance.get_qos_ids() == [3]
