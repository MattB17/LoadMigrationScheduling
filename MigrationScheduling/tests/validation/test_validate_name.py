import pytest
from MigrationScheduling.validation import validate_name
from MigrationScheduling import exceptions as exc


def test_valid_names():
    validate_name("s0", 's', "Switch")
    validate_name("c5", 'c', "Controller")
    validate_name("g15", 'g', "QoS Group")

def test_invalid_name_wrong_first_letter():
    with pytest.raises(exc.InvalidName):
        validate_name("h13", "s", "Switch")

def test_invalid_name_too_many_characters():
    with pytest.raises(exc.InvalidName):
        validate_name("grp3", "g", "QoS Group")

def test_invalid_name_float():
    with pytest.raises(exc.InvalidName):
        validate_name("c3.5", 'c', "Controller")
