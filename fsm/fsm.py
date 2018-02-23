class StateMachine:
    NO_STATE = 0
    TERMINATE_MACHINE = -1

    def __init__(self, states):
        self.states = states

        self.activeState = StateMachine.NO_STATE

        # Starting state is always the first of the list
        self.nextState = 1

    def getActiveState(self):
        return self.states[self.activeState]

    def update(self, T, dt):
        if self.nextState > StateMachine.NO_STATE:
            self.activeState = self.nextState
            self.nextState = StateMachine.NO_STATE
            self.getActiveState().onEntry(T, dt)

        self.nextState = self.getActiveState().update(T, dt)

        if self.nextState != StateMachine.NO_STATE:
            self.getActiveState().onExit(T, dt)
            return self.nextState != StateMachine.TERMINATE_MACHINE

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


class StateBase:
    def __init__(self, name, events=[]):
        self.name = name
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

    def collectTelemetry(self):
        """
        Returns a tuple containing the state telemetry id and a dictionary containing telemetry
        data for the last update.
        :return: tuple (state_id, {data_id_1: value1, ..., data_id_N: valueN})
        """
        raise NotImplemented

    def onExit(self, T, dt):
        for e in self.events:
            e.onExit(T, dt)



