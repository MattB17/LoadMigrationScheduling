class Migration:
    def __init__(self, switch, dst_controller, load):
        self._switch = switch
        self._dst_controller = dst_controller
        self._load = load
        self._groups = set()

    def get_switch(self):
        return self._switch

    def get_dst_controller(self):
        return self._dst_controller

    def get_load(self):
        return self._load

    def add_qos_group(self, group_name):
        self._groups.add(group_name)

    def get_groups(self):
        return self._groups

    def is_in_group(self, group_name):
        return group_name in self._groups
