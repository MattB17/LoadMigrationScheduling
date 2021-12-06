import pytest
from MigrationScheduling import specs
from MigrationScheduling import exceptions as exc
from MigrationScheduling.validation import validate_bottleneck_setting


def test_valid_settings():
    for setting in specs.BOTTLENECK_SETTINGS:
        validate_bottleneck_setting(setting)


def test_invalid_settings():
    with pytest.raises(exc.IncorrectBottleneckSetting):
        validate_bottleneck_setting("randomSetting")
    with pytest.raises(exc.IncorrectBottleneckSetting):
        validate_bottleneck_setting("someOtherSetting")
