class QosConstraint:
    def __init__(self, group, capacity):
        self._group = group
        self._capacity = capacity
        self._switches = set()

    def get_group(self):
        return self._group

    def get_capacity(self):
        return self._capacity

    def get_switches(self):
        return self._switches

    def add_switch(self, switch_name):
        self._switches.add(switch_name)
