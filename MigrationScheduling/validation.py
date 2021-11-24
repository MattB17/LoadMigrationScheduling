"""This module implements functions related to validation used to ensure
that objects are initialized properly or signal errors if not.

"""
from MigrationScheduling import exceptions as exc


def validate_name(proposed_name, first_letter, object_type):
    """Validates that `proposed_name` follows the proper naming convention.

    The correct naming convention for `proposed_name` for `object_type` is
    `first_letter` followed by an integer.

    Parameters
    ----------
    proposed_name: str
        A string representing the name being validated.
    first_letter: char
        A character representing the first character of a correct name.
    object_type: str
        A string representing the name of the object to which the name
        applies.

    Raises
    ------
    InvalidName
        If `proposed_name` does not follow the correct naming convention for
        `object_type`.

    Returns
    -------
    None

    """
    msg_str = ("{0} names should be in the form '{1}x' where " +
               "'x' is an ID. {2} does not meet this criteria").format(
               object_type, first_letter, proposed_name)
    if not len(proposed_name) or proposed_name[0] != first_letter:
        raise exc.InvalidName(msg_str)
    try:
        int(proposed_name[1:])
    except:
        raise exc.InvalidName(msg_str)


def validate_bottleneck_setting(supplied_setting):
    """Validates whether `supplied_setting` is a correct bottleneck setting.

    Correct bottleneck settings are 'high', 'medium', or 'low'

    Parameters
    ----------
    supplied_setting: str
        A string representing the bottleneck setting to be validated.

    Raises
    ------
    IncorrectBottleneckSetting
        If `supplied_setting` is not one of the correct bottleneck settings.

    Returns
    -------
    None

    """
    if supplied_setting not in {"low", "medium", "high"}:
        raise exc.IncorrectBottleneckSetting(supplied_setting)
