"""The `InstanceData` class contains all the data of a migration scheduling
instance used to construct an optimization model.

"""

class InstanceData:
    """Stores the data of a migration scheduling instance.

    Parameters
    ----------
    migrations: dict
        A dictionary specifying the migrations. The keys are strings denoting
        the name of the switch involved in the migration and the
        corresponding value is a `Migration` object specifying the migration.
    controller_consts: set
        A set of `ControllerConstraint` objects specifying the controller
        constraints for the migrations.
    qos_consts: set
        A set of `QosConstraint` objects specifying the QoS constraints.
    switch_ids: list
        A list of IDs of the switches involved in the migrations.
    round_ids: list
        A list of rounds in which migrations can be scheduled.
    controller_ids: list
        A list of IDs of the controllers in the controller constraints.
    qos_ids: list
        A list of IDs of the QoS groups.

    Attributes
    ----------
    _migrations: dict
        The migrations to be scheduled
    _controller_consts: set
        The controller constraints.
    _qos_consts: set
        The constraints for QoS groups.
    _switch_ids: list
        The IDs of the switches involved in the migrations.
    _round_ids: list
        The IDs of rounds in which migrations can be scheduled.
    _controller_ids: list
        The IDs of the destination controllers for migrations.
    _qos_ids: list
        The IDs of the QoS groups.

    """
    def __init__(self, migrations, controller_consts, qos_consts,
                 switch_ids, round_ids, controller_ids, qos_ids):
        self._migrations = migrations
        self._controller_consts = controller_consts
        self._qos_consts = qos_consts
        self._switch_ids = switch_ids
        self._round_ids = round_ids
        self._controller_ids = controller_ids
        self._qos_ids = qos_ids
