from fsm.fsm import StateMachine, StateBase, EventBase
from .common.states import AwaitLiftoffState
from .common.events import LandingEvent
from enum import IntEnum, unique
from ksp_krpc import vessel, conn


@unique
class GrasshopperStatesEnum(IntEnum):
    AwaitLiftoff = 1
    Powering = 2
    Descending = 3


class CountdownState(AwaitLiftoffState):
    def __init__(self):
        super().__init__("AWAIT LIFTOFF", 3, GrasshopperStatesEnum.Powering)

    def onEntry(self, T, dt):
        super().onEntry(T, dt)
        vessel.auto_pilot.target_pitch_and_heading(90, 90)
        vessel.auto_pilot.sas = True
        vessel.control.throttle = 0

    def update(self, T, dt):
        return super().update(T, dt)

    def onExit(self, T, dt):
        super().onExit(T, dt)


class EndPoweringEvent(EventBase):
    def __init__(self):
        super().__init__("GHEndPoweringEvent")
        self.altitude = None
        self.starting_alt = 0

    def onEntry(self, T, dt):
        self.altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')
        self.starting_alt = self.altitude()

    def check(self, T, dt):
        if self.altitude() - self.starting_alt > 5:
            return GrasshopperStatesEnum.Descending

        return StateMachine.NO_EVENT

    def onExit(self, T, dt):
        self.altitude.remove()


class PoweringState(StateBase):
    def __init__(self):
        super().__init__("POWERING", [EndPoweringEvent()])

    def onEntry(self, T, dt):
        super().onEntry(T, dt)
        vessel.control.throttle = 1
        vessel.control.activate_next_stage()

    def update(self, T, dt):
        return super().update(T, dt)

    def onExit(self, T, dt):
        super().onExit(T, dt)
        vessel.control.throttle = 0


class DescendingState(StateBase):
    def __init__(self):
        super().__init__("DESCENDING_STATE", [LandingEvent(StateMachine.TERMINATE_MACHINE)])

    def onEntry(self, T, dt):
        super().onEntry(T, dt)

    def update(self, T, dt):
        return super().update(T, dt)

    def onExit(self, T, dt):
        super().onExit(T, dt)


GrasshopperStates = {
    GrasshopperStatesEnum.AwaitLiftoff: CountdownState(),
    GrasshopperStatesEnum.Powering: PoweringState(),
    GrasshopperStatesEnum.Descending: DescendingState()
    }

