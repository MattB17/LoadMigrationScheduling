"""A module containing the Exception classes generated when building a
load migration schedule.

"""

class InvalidName(Exception):
    """Exception raised when an invalid object name is generated.

    Attributes
    ----------
    message: str
        A string representing the message displayed to the user.

    """
    def __init__(self, message):
        super().__init__(message)
