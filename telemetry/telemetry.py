from fsm.fsm import StateMachine
telemetry_unit = {}


class GroupBuilder:
    def __init__(self, groupname):
        self.groupname = groupname
        self.data = {}

    def addData(self, key, value):
        self.data[key] = value
        return self

    def build(self):
        return self.groupname + "_group", self.data


def addGroup(group):
    telemetry_unit[group[0]] = group[1]


def update(state_machine):
    collect(state_machine)


def collect(state_machine: StateMachine):
    addGroup(state_machine.collectTelemetry())


