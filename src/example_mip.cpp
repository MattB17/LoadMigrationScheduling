/* This example formulates and solve the following MIP:

   maximize     x +  y + 2z
   subject to   x + 2y + 3z <= 4
                x +  y      >= 1
                x, y, z binary
*/
#include "gurobi_c++.h"
#include <vector>

int main(int argc, char* argv[]) {
  try {
    // Create an environment
    GRBEnv env = GRBEnv(true);
    env.set("LogFile", "example_mip.log");
    env.start();

    // Create an empty model
    GRBModel model = GRBModel(env);

    // Create Variables
    GRBVar x = model.addVar(0.0, 1.0, 0.0, GRB_BINARY, "x");
    GRBVar y = model.addVar(0.0, 1.0, 0.0, GRB_BINARY, "y");
    GRBVar z = model.addVar(0.0, 1.0, 0.0, GRB_BINARY, "z");

    // Set Objective
    model.setObjective(x + y + 2*z, GRB_MAXIMIZE);

    // Add Constraints
    model.addConstr(x + 2*y + 3*z <= 4, "c0");
    model.addConstr(x + y >= 1, "c1")

    // Optimize model
    model.optimize();

    std::vector<GRBVar> variables {x, y, z};
    for (GRBVar var : variables) {
      std::cout << var.get(GRB_StringAttr_VarName) << " "
                << var.get(GRB_DoubleAttr_X) << std::endl;
    }
    std::cout << "Obj: " << model.get(GRB_DoubleAttr_ObjVal) << std::endl;
  } catch(GRBException e) {
    std::cout << "Error code = " << e.getErrorCode() << std::endl;
    std::cout << e.getMessage() << std::endl;
  } catch(...) {
    std::cout << "Exception during optimization" << std::endl;
  }

  return 0;
}
