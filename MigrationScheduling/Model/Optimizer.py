"""The `Optimizer` class is used to construct a model to optimize the load
migration schedule.

"""
from MigrationScheduling.Model import Parser

class Optimizer:
    """Builds an optimization model for a migration scheduling instance.

    Attributes
    ----------
    _model: gurobipy.Model
        A `Model` object representing the optimization model. A value of
        None indicates a model that has not been initialized.
    _parser: Parser
        A `Parser` object used to parse the migration scheduling instance. A
        value of None indicates that it has not been initialized.
    _switch_ids: list
        A list of the switch IDs involved in the migration.
    _round_ids: list
        A list of round IDs indicating the rounds in which a migration can be
        scheduled.
    _controller_ids: list
        A list of controller IDs corresponding for the controllers used in
        the controller capacity constraints.
    _group_ids: list
        A list of IDs of the QoS groups.

    """
    def __init__(self):
        self._model = None
        self._parser = None
        self._switch_ids = []
        self._round_ids = []
        self._controller_ids = []
        self._group_ids = []

    def get_model_data(self, migration_file):
        """Retrieves the data for the migration scheduling instance.

        A `Parser` is constructed and used to parse `migration_file` to
        retrieve the data of a migration scheduling instance to be
        optimized.

        Parameters
        ----------
        migration_file: str
            A string representing the path to the file specifying the load
            migration scheduling instance.

        Returns
        -------
        None
        
        """
        self._parser = Parser()
        self._parser.parse_migrations(migration_file)
