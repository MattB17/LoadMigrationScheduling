"""A set of specifications and global parameters used throughout the load
migration scheduling project.

"""

# index for new small instances
SMALL_IDX = 1

# index for new large instances
LARGE_IDX = 0

# cutoff for deciding whether an instance is small or large. The cutoff is
# in terms of number of migrations. Small instances can be solved directly
# with the optimizer, large instances require heuristic methods.
SMALL_CUTOFF = 250
