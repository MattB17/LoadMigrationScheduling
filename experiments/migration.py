"""Solve a load migrations scheduling instance.

"""
import gurobipy as gp
from gurobipy import GRB

# indices of network objects
switch_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
round_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
controller_ids = [0, 1, 2, 3, 4]
group_ids = [0, 1, 2, 3]

# switch loads
loads = {i: 1 for i in range(10)}

# controller capacities
controller_caps = {i: 1 for i in range(5)}

# group capacities
group_caps = {i: 1 for i in range(4)}

# switches migrating to each destination controller
dst_controllers = {0: {2},
                   1: {0, 7},
                   2: {3, 4},
                   3: {5, 6, 8},
                   4: {1, 9}}

# group membership
groups = {0: {0, 1, 5, 8},
          1: {1, 4, 7},
          2: {3, 6},
          3: {2, 3}}

m = gp.Model('migration')

x_vars = m.addVars(switch_ids, round_ids, vtype=GRB.BINARY, name="x")
lambda_var = m.addVar(name="lambda")

m.setObjective(lambda_var, GRB.MINIMIZE)

m.addConstrs((x_vars.sum(i, '*') == 1 for i in switch_ids), 'migrate')

m.addConstrs((r * x_vars[i, r] <= lambda_var
              for i in switch_ids for r in round_ids), "bounds")

m.addConstrs((sum(loads[i] * x_vars[i, r] for i in dst_controllers[j])
              <= controller_caps[j]
              for j in controller_ids for r in round_ids), "controller_cap")

m.addConstrs((sum(x_vars[i, r] for i in groups[l]) <= group_caps[l]
              for l in group_ids for r in round_ids), "group_cap")

m.optimize()

if m.status == GRB.OPTIMAL:
    solution = m.getAttr('x', x_vars)
    for r in round_ids:
        for i in switch_ids:
            if solution[i, r] > 0:
                print("Migration {0} in round {1}".format(i, r))
    print('Objective value: {0}'.format(m.objVal))
    print("Lambda: {0}".format(lambda_var.x))
