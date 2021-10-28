class ControllerConstraint:
    def __init__(self, controller, capacity):
        self._controller = controller
        self._capacity = capacity
        self._switches = set()

    def get_controller(self):
        return self._controller

    def get_capacity(self):
        return self._capacity

    def get_switches(self):
        return self._switches

    def add_switch(self, switch_name):
        self._switches.add(switch_name)
