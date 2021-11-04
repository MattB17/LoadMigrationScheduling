"""The `Optimizer` class is used to construct a model to optimize the load
migration schedule.

"""
from MigrationScheduling.Model import InstanceData, Parser
from MigrationScheduling import exceptions as exc
from MigrationScheduling import utils
import gurobipy as gp

class Optimizer:
    """Builds an optimization model for a migration scheduling instance.

    Attributes
    ----------
    _model: gurobipy.Model
        A `Model` object representing the optimization model. A value of
        None indicates a model that has not been initialized.
    _data: InstanceData
        An `InstanceData` object containing the data for the migration
        scheduling instance being modeled. A value of None indicates
        that the instance has not yet been specified.

    """
    def __init__(self):
        self._model = None
        self._data = None

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
        parser = Parser()
        parser.parse_migrations(migration_file)
        self._data = parser.to_data()

    def _initialize_variables(self, is_ip=True):
        """Initializes the variables for the optimization model.

        Parameters
        ----------
        is_ip: bool
            A boolean flag indicating whether it is an IP model. If true
            the variables will be integer, otherwise, they will be continuous.

        Returns
        -------
        gp.Var, gp.Vars
            A variable representing the parameter to be optimized and a
            collection of variables representing which round each migration
            is scheduled in.

        """
        if self._model:
            lambda_var = self._model.addVar(name="lambda")
            if is_ip:
                x_vars = self._model.addVars(
                    self._data.get_switch_ids(), self._data.get_round_ids(),
                    vtype=gp.GRB.BINARY, name="x")
            else:
                x_vars = self._model.addVars(
                    self._data.get_switch_ids(), self._data.get_round_ids(),
                    lb=0.0, ub=1.0, vtype=gp.GRB.CONTINUOUS, name="x")
            return lambda_var, x_vars
        raise exc.UninitializedModel()

    def _add_migrate_constraints(self, x_vars):
        """Adds the migrate constraints using `x_vars`.

        The migrate constraints enforces that each migration takes place
        in exactly one round.

        Parameters
        ----------
        x_vars: gp.Vars
            The set of model variables used in the migrate constraints.

        Returns
        -------
        None

        """
        self._model.addConstrs(
            (x_vars.sum(i, '*') == 1
             for i in self._data.get_switch_ids()), "migrate")

    def _add_bound_constraints(self, lambda_var, x_vars):
        """Adds the constraints bounding `lambda_var`.

        A constraint is introduced for each round and migration, enforcing
        the constraint that if migration i is scheduled in round r then
        `lambda_var` must be at least r.

        Parameters
        ----------
        lambda_var: gp.Var
            The variable that is being bounded.
        x_vars: gp.Vars
            The collection of variables used to bound `lambda_var`.

        Returns
        -------
        None

        """
        self._model.addConstrs(
            (r * x_vars[i, r] <= lambda_var
             for i in self._data.get_switch_ids()
             for r in self._data.get_round_ids()), "bound")

    def _add_controller_constraints(self, x_vars):
        """Adds the set of controller constraints to the model using `x_vars`.

        Parameters
        ----------
        x_vars: gp.Vars
            The set of model variables used in the controller constraints.

        Returns
        -------
        None

        """
        for controller_const in self._data.get_control_consts():
            for r in self._data.get_round_ids():
                self._model.addConstr(sum(
                    self._data.get_load(s) *
                    x_vars[self._data.get_switch_id(s), r]
                    for s in controller_const.get_switches()) <=
                    controller_const.get_capacity(),
                    "controller[{0}, {1}]".format(
                        controller_const.get_controller_idx(), r))

    def _add_qos_constraints(self, x_vars):
        """Adds the set of QoS constraints to the model using `x_vars`.

        Parameters
        ----------
        x_vars: gp.Vars
            The set of model variables used in the controller constraints.

        Returns
        -------
        None

        """
        for qos_const in self._data.get_qos_consts():
            for r in self._data.get_round_ids():
                self._model.addConstr(sum(
                    x_vars[self._data.get_switch_id(s), r]
                    for s in qos_const.get_switches()) <=
                    qos_const.get_capacity(),
                    "qos[{0}, {1}]".format(qos_const.get_group_idx(), r))

    def build_model(self, migration_file):
        self.get_model_data(migration_file)
        self._model = gp.Model("migration")
        lambda_var, x_vars = self._initialize_variables()
        self._model.setObjective(lambda_var, gp.GRB.MINIMIZE)
        self._add_migrate_constraints(x_vars)
        self._add_bound_constraints(lambda_var, x_vars)
        self._add_controller_constraints(x_vars)
        self._add_qos_constraints(x_vars)
        self._model.optimize()
