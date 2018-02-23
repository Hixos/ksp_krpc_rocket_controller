from fsm.fsm import StateMachine, StateBase, EventBase
from .common.states import AwaitLiftoffState
from .common.events import LandingEvent
from enum import IntEnum, unique
from ksp_krpc import vessel, conn, VesselStreams

from utils.control.pid import PIDController
from utils.vessel_utils import throttleFromTwr
from utils.physiscs_utils import gravitationalAcceleration


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
    def __init__(self, target_altitude, tolerance=0.05):
        super().__init__("GHEndPoweringEvent")
        self.target_altitude = target_altitude
        self.tolerance = tolerance

        self.altitude = None

    def onEntry(self, T, dt):
        self.altitude = VesselStreams.Flight.meanAltitudeStream()

    def check(self, T, dt):
        if abs(self.altitude() - self.target_altitude)/self.target_altitude < self.tolerance:
            return GrasshopperStatesEnum.Descending

        return StateMachine.NO_EVENT

    def onExit(self, T, dt):
        self.altitude.remove()


class PoweringState(StateBase):
    def __init__(self, target_altitude):
        super().__init__("POWERING", [EndPoweringEvent(target_altitude)])
        self.target_altitude = target_altitude
        self.pid = PIDController(30, 0, 0)
        self.pid.setSetpoint(1)

        self.altitude = None
        self.mass = None
        self.orbit_radius = None
        self.available_thrust = None

        self.GM = VesselStreams.Orbit.CelestialBody.gravitationalParameter()

    def onEntry(self, T, dt):
        super().onEntry(T, dt)
        self.altitude = VesselStreams.Orbit.apoapsisAltitudeStream()
        self.mass = VesselStreams.mass()
        self.orbit_radius = VesselStreams.Orbit.radiusStream()
        self.available_thrust = VesselStreams.availableThrust()

        # Activate engines
        vessel.control.activate_next_stage()

    def update(self, T, dt):
        target_twr = self.pid.update(self.altitude()/self.target_altitude, dt)

        g = gravitationalAcceleration(self.GM, self.orbit_radius())
        throttle = throttleFromTwr(target_twr, self.mass(), self.available_thrust(), g)

        vessel.control.throttle = throttle

        return super().update(T, dt)

    def onExit(self, T, dt):
        super().onExit(T, dt)
        vessel.control.throttle = 0

        # Close streams
        self.altitude.remove()
        self.mass.remove()
        self.orbit_radius.remove()
        self.available_thrust.remove()


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
    GrasshopperStatesEnum.Powering: PoweringState(20000),
    GrasshopperStatesEnum.Descending: DescendingState()
    }

