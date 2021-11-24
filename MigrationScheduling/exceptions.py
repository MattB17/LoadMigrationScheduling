"""A module containing the Exception classes generated when building a
load migration schedule.

"""

class InvalidName(Exception):
    """Exception raised when an invalid object name is generated.

    Parameters
    ----------
    message: str
        A string representing the message displayed to the user.

    """
    def __init__(self, message):
        super().__init__(message)

class UninitializedModel(Exception):
    """Exception raised when an model has not been initialized.

    The Exception is raised when a user tries to access a model that has
    not yet been initialized.

    """
    def __init__(self):
        super().__init__("Must initialize model before adding variables, " +
                         "an objective function, and constraints.")

class InstanceNotSpecified(Exception):
    """Exception raised when a load migration instance has not been specified.

    """
    def __init__(self):
        super().__init__("Load migration instance not specified. " +
                         "Must specify instance before building model or " +
                          "running an algorithm.")

class ModelNotOptimized(Exception):
    """Generated when accessing details of model that has not been optimized.

    """
    def __init__(self):
        super().__init__("Model has not been optimized. Must solve " +
                         "model before looking at results.")

class SwitchNotFound(Exception):
    """Generated when `switch_name` is not found in a queried object.

    Parameters
    ----------
    switch_name: str
        A string representing the name of the switch being searched for.

    """
    def __init__(self, switch_name):
        super().__init__("Switch {} not found.".format(switch_name))

class IncorrectBottleneckSetting(Exception):
    """Generated when `supplied_setting` is an incorrect bottleneck setting.

    The exception is generated when an incorrect bottleneck setting is used.
    A correct bottleneck setting is one of "high", "medium", or "low".

    Parameters
    ----------
    supplied_setting: str
        A string representing the supplied bottleneck setting that generated
        the exception.

    """
    def __init__(self, supplied_setting):
        super().__init__(
            "Incorrect bottleneck setting used: {}. Possible settings are " +
            "'high', 'medium', or 'low'.\n".format(supplied_setting))
