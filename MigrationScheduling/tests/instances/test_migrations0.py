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
CONTROLLER_IDS = [0, 1, 2, 3, 4]
GROUP_IDS = [0, 1, 2, 3]

# switch loads
LOADS = {i: 1 for i in range(10)}

# controller capacities
CONTROLLER_CAPS = {i: 1 for i in range(5)}

# group capacities
GROUP_CAPS = {i: 1 for i in range(4)}

# set of switches migrating to given destination controller
DST_CONTROLLERS = {0: {2},
                   1: {0, 7},
                   2: {3, 4},
                   3: {6, 8},
                   4: {1, 5, 9}}

# group membership
GROUPS = {0: {0, 1, 5, 8},
          1: {1, 4, 7},
          2: {3, 6},
          3: {2, 3}}

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
                  for j in CONTROLLER_IDS for r in ROUND_IDS
                  if len(DST_CONTROLLERS[j]) > 0),
                  "controller_cap")
    m.addConstrs((sum(x_vars[i, r] for i in GROUPS[l]) <= GROUP_CAPS[l]
                  for l in GROUP_IDS for r in ROUND_IDS),
                  "group_cap")
    m.optimize()

    # optimizer
    optimizer = Optimizer()
    optimizer.get_model_data(os.path.join(DIR,
        os.path.join("instances", "migrations0.txt")))
    optVal = optimizer.build_ip_model(verbose=False)
    assert round(optVal, 2) == round(m.objVal, 2)

def test_vff_heuristic():
    optimizer = Optimizer()
    optimizer.get_model_data(os.path.join(DIR,
        os.path.join("instances", "migrations0.txt")))
    vff_val = algorithms.vector_first_fit(optimizer.instance_data())

    # vff solution should be 4:
    # - migrations 0, 2, 4, 6, and 9 are scheduled in round 1
    # - migrations 1 and 3 are scheduled in round 2
    # - migrations 5 and 7 are scheduled in round 3
    # - migration 8 is scheduled in round 4
    assert vff_val == 4
