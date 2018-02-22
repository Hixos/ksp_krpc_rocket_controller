from fsm.fsm import StateBase
from .events import LiftoffEvent


# Copy this when creating new states
class EmptyState(StateBase):
    def __init__(self):
        super().__init__("EMPTY_STATE")

    def onEntry(self, T, dt):
        super().onEntry(T, dt)

    def update(self, T, dt):
        return super().update(T, dt)

    def onExit(self, T, dt):
        super().onExit(T, dt)


class AwaitLiftoffState(StateBase):
    def __init__(self, name, countdown_length, next_state_id):
        super().__init__(name, [LiftoffEvent(countdown_length, next_state_id)])

    def onEntry(self, T, dt):
        super().onEntry(T, dt)

    def update(self, T, dt):
        return super().update(T, dt)

    def onExit(self, T, dt):
        super().onExit(T, dt)
