import os
import gurobipy as gp
from gurobipy import GRB
from MigrationScheduling import algorithms
from MigrationScheduling.Model import Optimizer

DIR = os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# indices of network objects
SWITCH_IDS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
ROUND_IDS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
CONTROLLER_IDS = [0, 2, 3, 4, 5, 6]
GROUP_IDS = [0, 1, 2, 3, 4, 5, 6]

# switch loads
LOADS = {0: 299.72,
         1: 112.63,
         2: 314.46,
         3: 71.78,
         4: 346.62,
         5: 272.62,
         6: 123.08,
         7: 280.35,
         8: 343.59,
         9: 296.22}

# controller capacities
CONTROLLER_CAPS = {0: 123.08,
                   2: 544.57,
                   3: 71.78,
                   4: 817.72,
                   5: 272.62,
                   6: 372.52}

# group capacities
GROUP_CAPS = {0: 3, 1: 2, 2: 2, 3: 2, 4: 2, 5: 3, 6: 5}

# switches migrating to each destination controller
DST_CONTROLLERS = {0: {6},
                   2: {4, 9},
                   3: {3},
                   4: {0, 1, 7},
                   5: {5},
                   6: {2, 8}}

# group membership
GROUPS = {0: {3, 7, 8},
          1: {3, 4, 8},
          2: {3, 4, 6, 7, 8},
          3: {0, 2, 6},
          4: {0, 1, 3, 7},
          5: {0, 7, 8},
          6: {1, 3, 6, 7, 8}}


def test_optimizer():
    # direct modelling
    m = gp.Model('test-migration')
    x_vars = m.addVars(SWITCH_IDS, ROUND_IDS, vtype=GRB.BINARY, name="x")
    lambda_var = m.addVar(name="lambda")
    m.setObjective(lambda_var, GRB.MINIMIZE)
    m.addConstrs((x_vars.sum(i, '*') == 1 for i in SWITCH_IDS), 'migrate')
    m.addConstrs((r * x_vars[i, r] <= lambda_var
                  for i in SWITCH_IDS for r in ROUND_IDS), "bounds")
    m.addConstrs((sum(LOADS[i] * x_vars[i, r] for i in DST_CONTROLLERS[j])
                  <= CONTROLLER_CAPS[j]
                  for j in CONTROLLER_IDS for r in ROUND_IDS),
                  "controller_cap")
    m.addConstrs((sum(x_vars[i, r] for i in GROUPS[l]) <= GROUP_CAPS[l]
                  for l in GROUP_IDS for r in ROUND_IDS),
                  "group_cap")
    m.optimize()

    # optimizer
    optimizer = Optimizer()
    optimizer.get_model_data(os.path.join(DIR,
        os.path.join("instances", "migrations2.txt")))
    optVal = optimizer.build_ip_model(verbose=False)
    assert round(optVal, 2) == round(m.objVal, 2)

def test_vff_heuristic():
    optimizer = Optimizer()
    optimizer.get_model_data(os.path.join(DIR,
        os.path.join("instances", "migrations2.txt")))
    vff_val = algorithms.vector_first_fit(optimizer.instance_data())

    # the VFF solution has value 3:
    # - migrations 0, 1, 2, 4, and 5 are scheduled in round 1
    # - migrations 3, 6, and 9 are scheduled in round 2
    # - migrations 7 and 8 are scheduled in round 3
    assert vff_val == 3
