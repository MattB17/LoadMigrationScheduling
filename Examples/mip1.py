#! /usr/bin/env python3.6
"""This example formulates and solves the following MIP model:
        max x + y + 2z
    s.t.
        x + 2y + 3z <= 5
        x +  y      >= 1
        x, y, z binary

"""
import gurobipy as gp
from gurobipy import GRB

if __name__ == "__main__":
    try:
        m = gp.Model("mip1") # create a new model

        # create variables
        x = m.addVar(vtype=GRB.BINARY, name="x")
        y = m.addVar(vtype=GRB.BINARY, name="y")
        z = m.addVar(vtype=GRB.BINARY, name="z")

        # set objective
        m.setObjective(x + y + 2 * z, GRB.MAXIMIZE)

        # Add constraints
        m.addConstr(x + 2*y + 3*z <= 4, "c0")
        m.addConstr(x + y >= 1, "c1")

        # Optimize model
        m.optimize()

        # print variables
        for v in m.getVars():
            print('{0}: {1}'.format(v.varName, v.x))

        print('Objective value: {0}'.format(m.objVal))
    except gp.GurobiError as e:
        print("Error code {0}: {1}".format(e.errno, e))
    except AttributeError:
        print("Encountered an attribute error")
