class StateMachine:
    NO_EVENT = 0
    TERMINATE_MACHINE = -1

    def __init__(self, states, T, dt):
        self.states = states

        # Starting state is always the first of the list
        self.activeState = 1
        self.enteredActiveState = False
        self.enterActiveState(T, dt)

    def getActiveState(self):
        return self.states[self.activeState]

    def enterActiveState(self, T, dt):
        print("Entering state " + self.activeStateName())
        self.getActiveState().onEntry(T, dt)
        self.enteredActiveState = True

    def exitActiveState(self, T, dt):
        print("Exiting state " + self.activeStateName())
        self.getActiveState().onExit(T, dt)

    def transitionToState(self, T, dt, state):
        self.exitActiveState(T, dt)
        self.activeState = state
        self.enteredActiveState = False

    def update(self, T, dt):
        if not self.enteredActiveState:
            self.enterActiveState(T, dt)
        new_state = self.getActiveState().update(T, dt)
        if new_state == self.TERMINATE_MACHINE:
            self.exitActiveState(T, dt)
            return False
        elif new_state == self.NO_EVENT:
            return True
        elif new_state in self.states.keys():
            self.transitionToState(T, dt, new_state)
            return True

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
        return StateMachine.NO_EVENT

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
            if result != StateMachine.NO_EVENT:
                return result

        return StateMachine.NO_EVENT

    def onExit(self, T, dt):
        for e in self.events:
            e.onExit(T, dt)



