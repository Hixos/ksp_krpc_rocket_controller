from telemetry.telemetry import TelemetryProviderInterface, TelemetryBuilder, addProvider


class StateMachine(TelemetryProviderInterface):
    NO_STATE = 0
    TERMINATE_MACHINE = -1

    def __init__(self, states):
        self.states = states

        # Starting state is always the first of the list
        self.activeState = 1
        self.entered_active_state = False

        self.nextState = StateMachine.NO_STATE

    def getActiveState(self):
        return self.states[self.activeState]

    def enterActiveState(self, T, dt):
        self.getActiveState().onEntry(T, dt)
        self.entered_active_state = True
        print("{} on Entry".format(self.getActiveState().getName()))

    def exitActiveState(self, T, dt):
        self.getActiveState().onExit(T, dt)
        self.entered_active_state = False
        print("{} on Exit".format(self.getActiveState().getName()))

    def update(self, T, dt):
        if self.nextState > StateMachine.NO_STATE:
            self.exitActiveState(T, dt)
            self.activeState = self.nextState
            self.nextState = StateMachine.NO_STATE

        if not self.entered_active_state:
            self.enterActiveState(T, dt)

        self.nextState = self.getActiveState().update(T, dt)

        return self.nextState != StateMachine.TERMINATE_MACHINE

    def getProviderKey(self):
        return "active_state"

    def provideTelemetry(self):
        return self.getActiveState().provideTelemetry()

    def terminate(self, T, dt):
        self.exitActiveState(T, dt)

    def activeStateName(self):
        return self.states[self.activeState].getName()


class EventBase:
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    def onEntry(self, T, dt):
        pass

    def check(self, T, dt):
        return StateMachine.NO_STATE

    def onExit(self, T, dt):
        pass


class StateBase(TelemetryProviderInterface):
    def __init__(self, name, events=[]):
        self.name = name + "_state"
        self.events = events

    def addEvent(self, event):
        self.events.append(event)

    def getName(self):
        return self.name

    def onEntry(self, T, dt):
        for e in self.events:
            e.onEntry(T, dt)

    def update(self, T, dt):
        for e in self.events:
            result = e.check(T, dt)
            if result != StateMachine.NO_STATE:
                return result

        return StateMachine.NO_STATE

    def getKey(self):
        return self.getName()

    def provideTelemetry(self):
        # Return empty data as default
        return TelemetryBuilder(self.getName()).build()

    def onExit(self, T, dt):
        for e in self.events:
            e.onExit(T, dt)



