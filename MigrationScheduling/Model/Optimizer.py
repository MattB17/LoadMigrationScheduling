"""The `Optimizer` class is used to construct a model to optimize the load
migration schedule.

"""
from MigrationScheduling.Data import InstanceData
from MigrationScheduling.Model import Parser
from MigrationScheduling import exceptions as exc
from MigrationScheduling import utils
import gurobipy as gp
import numpy as np

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

    def instance_data(self):
        """The data for the load migration scheduling instance being modeled.

        Returns
        -------
        InstanceData
            An `InstanceData` object specifying the data for a load migration
            scheduling instance.

        """
        return self._data

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

    def build_ip_model(self, verbose=True):
        """Builds an Integer Programming model for the migration instance.

        The model is instantiated and solved based on the pre-loaded instance
        of the load migration scheduling problem.

        Parameters
        ----------
        verbose: bool
            A boolean indicating whether verbose mode is used. If used the
            entire solution will be printed, otherwise, only gurobi messages
            will be printed. The default value is True.

        Raises
        ------
        InstanceNotSpecified
            If a migration scheduling instance has not yet been specified.

        Returns
        -------
        float
            A float representing the best objective value found during
            optimization.

        """
        return self._build_model(is_ip=True, verbose=verbose)

    def build_lp_model(self, verbose=True):
        """Builds a Linear Programming model for the migration instance.

        The model is instantiated and solved based on the pre-loaded instance
        of the load migration scheduling problem.

        Parameters
        ----------
        verbose: bool
            A boolean indicating whether verbose mode is used. If used the
            entire solution will be printed, otherwise, only gurobi messages
            will be printed. The default value is True.

        Raises
        ------
        InstanceNotSpecified
            If a migration scheduling instance has not yet been specified.

        Returns
        -------
        float
            A float representing the best objective value found during
            optimization.

        """
        return self._build_model(is_ip=False, verbose=verbose)

    def get_model_bounds(self):
        """Computes upper and lower bounds for the model.

        The upper bound is computed by taking one round per migration. The
        lower bound is the solution to the linear program.

        Returns
        -------
        int, int
            An integer representing a lower bound on the number of rounds to
            complete all migrations and an integer representing an upper
            bound on the number of rounds to complete all migrations.

        """
        if self._data:
            ub = len(self._data.get_round_ids())
            self._build_model(is_ip=False, verbose=False)
            lb = int(np.ceil(self._model.objVal)) + 1
            return lb, ub
        raise exc.InstanceNotSpecified()

    def _initialize_variables(self, is_ip=True):
        """Initializes the variables for the optimization model.

        Parameters
        ----------
        is_ip: bool
            A boolean flag indicating whether it is an IP model. If true
            the variables will be integer, otherwise, they will be continuous.

        Raises
        ------
        UninitializedModel
            If the optimization model has not yet been initialized

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
        self._model.addConstrs((sum(
            self._data.get_load(s) * x_vars[self._data.get_switch_id(s), r]
            for s in control_const.get_switches()) <= control_const.get_cap()
            for control_const in self._data.get_control_consts()
            for r in self._data.get_round_ids()), "controller")

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
                    for s in qos_const.get_switches()) <= qos_const.get_cap(),
                    "QoS[{0}, {1}]".format(qos_const.get_group_idx(), r))

    def _add_constraints(self, lambda_var, x_vars):
        """Adds all constraints to the model using `lambda_var` and `x_vars`.

        Parameters
        ----------
        lambda_var: gp.Var
            The variable to be minimized, representing the maximum number
            of rounds required.
        x_vars: gp.Vars
            A collection of boolean variables for each migration and round
            pair, indicating if the migration is scheduled in that round.

        Raises
        ------
        UninitializedModel
            If the optimization model has not yet been initialized.

        Returns
        -------
        None

        """
        if self._model:
            self._add_migrate_constraints(x_vars)
            self._add_bound_constraints(lambda_var, x_vars)
            self._add_controller_constraints(x_vars)
            self._add_qos_constraints(x_vars)
        else:
            raise exc.UninitializedModel()

    def _build_model(self, is_ip=True, verbose=True):
        """Builds the optimization album for `migration_file`.

        The data is loaded from `migration_file` and an optimization model
        is built and solved for the specified instance. The model is an
        integer program is `is_ip` is True. Otherwise, it is a linear program.

        Parameters
        ----------
        is_ip: bool
            A boolean flag indicating whether it is an IP model. If true
            the variables will be integer, otherwise, they will be continuous.
        verbose: bool
            A boolean indicating whether verbose mode is used. If used the
            entire solution will be printed, otherwise, only gurobi messages
            will be printed.

        Raises
        ------
        InstanceNotSpecified
            If a migration scheduling instance has not yet been specified.
        ModelNotOptimized
            If the optimization model cannot be optimized.

        Returns
        -------
        float
            A float representing the best objective value found during
            optimization.

        """
        if self._data:
            self._model = gp.Model("migration")
            lambda_var, x_vars = self._initialize_variables(is_ip)
            self._model.setObjective(lambda_var, gp.GRB.MINIMIZE)
            self._add_constraints(lambda_var, x_vars)
            self._model.optimize()
            if verbose:
                self._print_output(x_vars, is_ip)
            return self._get_objective_value()
        else:
            raise exc.InstanceNotSpecified()

    def _print_solution(self, solution, is_binary=True):
        """Prints the model solution given by `solution`.

        The values of `solution` are printed specifying which round(s) each
        migration is scheduled in. If `is_binary` is True, each migration
        is scheduled in exactly one round, otherwise, the solution has
        fractional values.

        Parameters
        ----------
        solution: list
            An array containing the value of the x variables for each
            migration and round combination.
        is_binary: bool
            A boolean value indicating whether `solution` is a binary
            solution.

        Returns
        -------
        None

        """
        for r in self._data.get_round_ids():
            for i in self._data.get_switch_ids():
                if solution[i, r] > 0:
                    if is_binary:
                        print("Migration {0} in round {1}".format(i, r))
                    else:
                        print("x[{0}, {1}]: {2}".format(i, r, solution[i, r]))

    def _print_output(self, x_vars, is_ip=True):
        """Print the results of fitting the model.

        Parameters
        ----------
        x_vars: gp.Vars
            The set of model variables indicating in which round each
            migration is scheduled.
        is_ip: bool
            A boolean value indicating whether or not the model is an
            integer program.

        Raises
        ------
        ModelNotOptimized
            If the optimization model has not yet been solved.

        Returns
        -------
        None

        """
        if self._model and self._model.status == gp.GRB.OPTIMAL:
            solution = self._model.getAttr("x", x_vars)
            self._print_solution(solution, is_ip)
            print("Number of Rounds: {0}".format(self._model.objVal + 1))
        else:
            raise exc.ModelNotOptimized()

    def _get_objective_value(self):
        """The objective value of the model.

        Raises
        ------
        ModelNotOptimized
            If the model has not been optimized.

        Returns
        -------
        float
            A float representing the objective value of the model.

        """
        if self._model and self._model.status == gp.GRB.OPTIMAL:
            return self._model.objVal
        else:
            raise exc.ModelNotOptimized()
