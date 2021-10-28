class Parser:
    def __init__(self):
        self._migrations = {}
        self._controller_constraints = set()
        self._qos_constraints = set()

    def add_migration(self, migration_data):
        migration = Migration(
            migration_data[0], migration_data[1], float(migration_data[2]))
        curr_idx = 3
        n = len(migration_data)
        while (curr_idx < n):
            migration.add_qos_group(migration_data[curr_idx])
            curr_idx += 1
        self._migrations[migration_data[0]] = migration

    def add_controller_constraint(self, controller_data):
        constraint = ControllerConstraint(
            controller_data[0], float(controller_data[1]))
        for migration in self._migrations:
            if migration.get_dst_controller() == controller_data[0]:
                constraint.add_switch(migration.get_switch())
        self._controller_constraints.add(constraint)

    def add_qos_constraint(self, qos_data):
        constraint = QosConstraint(qos_data[0], qos_data[1])
        for migration in self._migrations:
            if migration.is_in_group(qos_data[0]):
                constraint.add_switch(migration.get_switch())
        self._qos_constraints.add(constraint)

    def parse_migrations(self, migration_file):
        with open(migration_file, 'r') as data_file:
            for line in data_file:
                if (line[0] == "s"):
                    self.add_migration(line.strip().split(" "))
                elif (line[0] == "c"):
                    self.add_controller_constraint(line.strip().split(" "))
                elif (line[0] == "g"):
                    self.add_qos_constraint(line.strip().split(" "))
        return
