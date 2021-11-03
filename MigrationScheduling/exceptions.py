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
                         "an objective function, and constraints")
