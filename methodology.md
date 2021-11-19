# Experimental Methodology
3 types of experiments to show need for CBF
* low bottleneck
  * for a given group `g` if `g` has `|g|` elements then its capacity is taken from a normal distribution with mean `0.5|g|` and standard deviation `0.3|g|`
  * for a given controller `c` if the load on `c` is `l` then the load is at least the maximum load of any migration on `c` (`l_max`) plus a positive value drawn from the normal distribution with mean `0.5(l - l_max)` and standard deviation `0.3(l - l_max)`
* medium bottleneck
  * for a given group `g` if `g` has `|g|` elements then its capacity is taken from a normal distribution with mean `0.2|g|` and standard deviation `0.3|g|`
  * for a given controller `c` if the load on `c` is `l` then the load is at least the maximum load of any migration on `c` (`l_max`) plus a positive value drawn from the normal distribution with mean `0.2(l - l_max)` and standard deviation `0.3(l - l_max)`
* high bottleneck
  * for all groups `g` we make the capacity as low as possible while still being feasible (so capacity 1)
  * for all controllers `c` we make the capacity as low as possible while still
  being feasible so we make it equal to the maximum load of any migration destined to the controller `l_max`

3 types of experiments to show need for heuristics
* small
  * number of migrations is between 5 and 200
* medium
  * number of migrations is between 201 and 1000
* large
  * number of migrations is between 1000 and 10000

Also add a few instances in the range 10000 to 1000000 and show heuristics perform reasonably well
