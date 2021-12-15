import os
import gurobipy as gp
from gurobipy import GRB
from MigrationScheduling import algorithms
from MigrationScheduling.Model import Optimizer

DIR = os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# indices of network objects
SWITCH_IDS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
ROUND_IDS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
CONTROLLER_IDS = [0, 1, 2, 3, 4]
GROUP_IDS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# switch loads
LOADS = {0: 13.24,
         1: 8.83,
         2: 17.9,
         3: 7.65,
         4: 7.68,
         5: 11.21,
         6: 1.38,
         7: 4.94,
         8: 5.46,
         9: 17.33,
         10: 10.34,
         11: 7.28,
         12: 4.25,
         13: 7.00,
         14: 6.99}

# controller capacities
CONTROLLER_CAPS = {0: 50.19,
                   1: 23.19,
                   2: 51.41,
                   3: 11.78,
                   4: 38.35}

# group capacities
GROUP_CAPS = {0: 1, 1: 1, 2: 2, 3: 5, 4: 2, 5: 1, 6: 1, 7: 1, 8: 1, 9: 2}

# switches migrating from each source controller
SRC_CONTROLLERS = {0: {0, 1, 5, 6, 8, 10, 14},
                   1: {2, 4, 11},
                   2: {3, 7, 13},
                   3: {12},
                   4: {9}}

# switches migrating to each destination controller
DST_CONTROLLERS = {0: {2, 3},
                   1: {13, 14},
                   2: {4, 6, 8, 9, 11, 12},
                   3: {5},
                   4: {0, 1, 7, 10}}

# group membership
GROUPS = {0: {0, 7, 14},
          1: {0, 1, 2, 3, 4, 7, 11, 14},
          2: {0, 3, 12, 14},
          3: {0, 1, 2, 7, 9, 11, 14},
          4: {0, 2, 13, 14},
          5: {0, 3, 12, 14},
          6: {0, 2, 3, 14},
          7: {7, 12, 14},
          8: {0, 2, 14},
          9: {0, 2, 3, 9, 11, 12, 14}}


def test_optimizer_without_resiliency():
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
        os.path.join("instances", "migrations3.txt")))
    optVal = optimizer.build_ip_model(resiliency=False, verbose=False)
    assert round(optVal, 2) == round(m.objVal, 2)

def test_optimizer_with_resiliency():
    # direct modelling
    m = gp.Model('test-migration')
    x_vars = m.addVars(SWITCH_IDS, ROUND_IDS, vtype=GRB.BINARY, name="x")
    lambda_var = m.addVar(name="lambda")
    m.setObjective(lambda_var, GRB.MINIMIZE)
    m.addConstrs((x_vars.sum(i, '*') == 1 for i in SWITCH_IDS), 'migrate')
    m.addConstrs((r * x_vars[i, r] <= lambda_var
                  for i in SWITCH_IDS for r in ROUND_IDS), "bounds")
    m.addConstrs((sum(LOADS[i] * x_vars[i, r]
                  for i in SRC_CONTROLLERS[j].union(DST_CONTROLLERS[j]))
                  <= CONTROLLER_CAPS[j]
                  for j in CONTROLLER_IDS for r in ROUND_IDS
                  if (len(SRC_CONTROLLERS[j]) > 0 or
                      len(DST_CONTROLLERS[j]) > 0)),
                  "controller_cap")
    m.addConstrs((sum(x_vars[i, r] for i in GROUPS[l]) <= GROUP_CAPS[l]
                  for l in GROUP_IDS for r in ROUND_IDS),
                  "group_cap")
    m.optimize()

    # optimizer
    optimizer = Optimizer()
    optimizer.get_model_data(os.path.join(DIR,
        os.path.join("instances", "migrations3.txt")))
    optVal = optimizer.build_ip_model(resiliency=True, verbose=False)
    assert round(optVal, 2) == round(m.objVal, 2)

def test_vff_heuristic():
    optimizer = Optimizer()
    optimizer.get_model_data(os.path.join(DIR,
        os.path.join("instances", "migrations3.txt")))
    vff_val = algorithms.vector_first_fit(optimizer.instance_data())

    # the VFF solution has value 8:
    # - migrations 0, 5, 6, 8, 9, 10, and 13 are scheduled in round 1
    # - migrations 1, and 12 are scheduled in round 2
    # - migration 2 is scheduled in round 3
    # - migration 3 is scheduled in round 4
    # - migration 4 is scheduled in round 5
    # - migration 7 is scheduled in round 6
    # - migration 11 is scheduled in round 7
    # - migration 14 is scheduled in round 8
    assert vff_val == 8
