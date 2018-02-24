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


def update(state_machine, T, dt):
    # Reset telemetry
    global telemetry_unit
    telemetry_unit = {}

    collect(state_machine, T, dt)

    print(telemetry_unit)


def collect(state_machine: StateMachine, T ,dt):
    basic = GroupBuilder('basic')
    basic.addData('ut', global_streams.ut())
    basic.addData('T', T)
    basic.addData('dt', dt)

    addGroup(basic.build())
    addGroup(state_machine.collectTelemetry())


