# Load Migration Scheduling

This work implements Optimization Models and heuristic methods to solve instances of the load migration scheduling problem. The problem was first detailed [here](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=8888045&casa_token=Tvo2TyUIhLcAAAAA:f7sVKCnmGGENb54-ZnlK2vJV0gmh0xVAJH7iMciFClFQfUZJdUvobKFpO81uVkhTwqMMqmM3&tag=1)

To install the package execute the following:
* `git clone https://github.com/MattB17/LoadMigrationScheduling.git`
* `cd LoadMigrationScheduling`
* `python -m pip install -r requirements.txt`
* `python -m pip install .`
  * you can alternatively add the `-e` option to install the package in edit mode.

### Simulating Instances
To simulate load migration scheduling options there are four options found in the `Scripts/simulation` folder:
* `sim_gaussian.py`
  * simulates load migration scheduling instances using Gaussian distributions
  * to run the script: `python Scrips/simulation/sim_gaussian.py <output_dir> <num_instances> <min_size> <max_size> <bottleneck_type>`
  * the arguments are as follows:
    * `<output_dir>` - the path to the directory in which the files will be output
    * `<num_instances>` - the number of instances to simulate
    * `<min_size>` - the minimum number of migrations for an instance
    * `<max_size>` - the maximum number of migrations for an instance
    * `<bottleneck_type>` - the bottleneck setting that adjusts the RHS of the constraints. Valid options are "low", "medium", and "high"
  * the simulator will generate `<num_instances>` instances with the number of migrations sampled uniformly at random in the interval [`<min_size>`, `<max_size>`]
* `sim_weighted_gaussian.py`
  * simulates load migration scheduling instances using weighted Gaussian distributions
  * for each controller and QoS constraint the capacity is sampled from one of 3 Gaussian distributions (representing low, medium, and high bottleneck) according to the supplied proportions
  * to run the script: `python Scrips/simulation/sim_weighted_gaussian.py <output_dir> <num_instances> <min_size> <max_size> <low_prop> <med_prop>`
  * the arguments are as follows:
    * `<output_dir>` - the path to the directory in which the files will be output
    * `<num_instances>` - the number of instances to simulate
    * `<min_size>` - the minimum number of migrations for an instance
    * `<max_size>` - the maximum number of migrations for an instance
    * `<low_prop>` - the proportion of constraints sampled from the low bottleneck Gaussian distribution
    * `<med_prop>` - the proportion of constraints sampled from the medium bottleneck Gaussian distribution
  * the simulator will generate `<num_instances>` instances with the number of migrations sampled uniformly at random in the interval [`<min_size>`, `<max_size>`]
* `sim_log_normal.py`
  * simulates load migration scheduling instances using a log normal distribution
  * the migration loads as well as the controller and QoS capacities are sampled from a log normal distribution
  * to run the script: `python Scrips/simulation/sim_log_normal.py <output_dir> <num_instances> <min_size> <max_size> <mu> <sigma>`
  * the arguments are as follows:
    * `<output_dir>` - the path to the directory in which the files will be output
    * `<num_instances>` - the number of instances to simulate
    * `<min_size>` - the minimum number of migrations for an instance
    * `<max_size>` - the maximum number of migrations for an instance
    * `<mu>` - the mean of the log normal distribution sampled from
    * `<sigma>` - the standard deviation of the log normal distribution sampled from
  * the simulator will generate `<num_instances>` instances with the number of migrations sampled uniformly at random in the interval [`<min_size>`, `<max_size>`]
* `sim_bounded_pareto.py`
  * simulates load migration scheduling instances using a bounded pareto distribution
  * the controller and QoS capacities are sampled from a bounded pareto distribution
  * to run the script: `python Scrips/simulation/sim_bounded_pareto.py <output_dir> <num_instances> <min_size> <max_size> <alpha>`
    * the arguments are as follows:
      * `<output_dir>` - the path to the directory in which the files will be output
      * `<num_instances>` - the number of instances to simulate
      * `<min_size>` - the minimum number of migrations for an instance
      * `<max_size>` - the maximum number of migrations for an instance
      * `<alpha>` - the alpha value for the pareto distribution (aka the shape parameter)
    * the simulator will generate `<num_instances>` instances with the number of migrations sampled uniformly at random in the interval [`<min_size>`, `<max_size>`]

The simulation scripts output files of the form `migration<x>.txt` where `<x>` is an index
* by default, the indices start at 0 and increment by 1
* you can change the starting index by changing the appropriate variable in `MigrationScheduling/specs.py`

### Solving Instances
There are two options for solving migration scheduling instances found in the `Scripts/solution` folder:
* `solve_single` - used to solve a single load migration scheduling instance
  * the results are printed to the screen and is primarily used for testing
  * run the script with `python Scripts/solution/solve_single.py <file> <run_optimizer>`
  * the arguments are as follows:
    * `<file>` - the path to the file being solved
    * `<run_optimizer>` - a boolean flag indicating whether to also run the optimizer. A value of "false" signals that just the heuristics will be run while a value of "true" signals the heuristics and optimizer will be run.
* `solve_bulk` - used to solve a group of load migration scheduling instances
  * the results will be output to a file called `results.txt` which has one row per instance
  * run the script with `python Scripts/solution/solve_bulk.py <input_dir> <output_dir> <file_pattern> <run_optimizer>`
  * the arguments are as follows:
    * `<input_dir>` - the path to the directory containing the instance files
    * `<output_dir>` - the path to the directory to which the results will be output
    * `<file_pattern>` - the file pattern of the input files. If a simulator was used to generate the files then the pattern will be "migration".
    * `<run_optimizer>` - a boolean flag indicating whether to also run the optimizer. A value of "false" signals that just the heuristics will be run while a value of "true" signals the heuristics and optimizer will be run.
