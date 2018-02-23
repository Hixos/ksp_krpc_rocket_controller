from fsm.fsm import StateMachine

from global_streams import global_streams

telemetry_unit = {}


class GroupBuilder:
    def __init__(self, group_name):
        self.group_name = group_name
        self.data = {}

    def addData(self, key, value):
        self.data[key] = value
        return self

    def build(self):
        return self.group_name + "_group", self.data


def addGroup(group):
    telemetry_unit[group[0]] = group[1]


def update(state_machine):
    collect(state_machine)

    print(telemetry_unit)


def collect(state_machine: StateMachine):
    basic = GroupBuilder('basic')
    basic.addData('ut', global_streams.ut())

    addGroup(basic.build())
    addGroup(state_machine.collectTelemetry())


