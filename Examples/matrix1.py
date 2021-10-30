#!/usr/bin/env python3.6
"""This example formulates and solves the following simple MIP model using the
matrix API:
        max x + y + 2z
    s.t.
        x + 2y + 3z <= 4
        x +  y      >= 1
        x, y, z binary

"""
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import scipy.sparse as sp

if __name__ == "__main__":
    try:
        # create a new model
        m = gp.Model("matrix1")

        # create variables
        x = m.addMVar(shape=3, vtype=GRB.BINARY, name="x")

        # set objective
        # @ operator is for dot product
        obj = np.array([1.0, 1.0, 2.0])
        m.setObjective(obj @ x, GRB.MAXIMIZE)

        # build (sparse) constraint matrix
        # val contains the 5 non-zero values (the second constraint)
        # is multiplied by -1 to make it a less than constraint
        # row and col give the row and column indices of the 5 non-zero
        # values
        val = np.array([1.0, 2.0, 3.0, -1.0, -1.0])
        row = np.array([0, 0, 0, 1, 1])
        col = np.array([0, 1, 2, 0, 1])

        A = sp.csr_matrix((val, (row, col)), shape=(2, 3))

        # build RHS vector
        rhs = np.array([4.0, -1.0])

        # Add constraints
        m.addConstr(A @ x <= rhs, name="c")

        # Optimize model
        m.optimize()

        # print variables and objective value
        print(x.X)
        print("Objective value: {0}".format(m.objVal))
    except gp.GurobiError as e:
        print("Error code {0}: {1}".format(e.errno, e))
    except AttributeError:
        print("Encountered an attribute error")
