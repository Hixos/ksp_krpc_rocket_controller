from ksp_krpc import vessel, VesselStreams
from fsm.fsm import StateMachine, StateBase, EventBase
from telemetry.telemetry import TelemetryBuilder

from enum import IntEnum, unique

from .common.states import AwaitLiftoffState
from .common.events import LandingEvent, AtApoapsisEvent

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
        super().__init__("countdown", 3, GrasshopperStatesEnum.Powering)

    def onEntry(self, T, dt):
        super().onEntry(T, dt)
        vessel.auto_pilot.target_pitch_and_heading(90, 90)
        vessel.auto_pilot.sas = True
        vessel.control.throttle = 0

    def update(self, T, dt):
        return super().update(T, dt)

    def onExit(self, T, dt):
        super().onExit(T, dt)


class AscendingState(StateBase):
    def __init__(self, target_altitude):
        super().__init__("ascending", [AtApoapsisEvent(GrasshopperStatesEnum.Descending, 2, target_altitude)])
        self.target_altitude = target_altitude
        self.pid = PIDController(15, 0, 0)
        self.pid.setSetpoint(1)

        self.apo_altitude = None
        self.mass = None
        self.orbit_radius = None
        self.available_thrust = None

        self.GM = VesselStreams.Orbit.CelestialBody.gravitationalParameter()

    def onEntry(self, T, dt):
        super().onEntry(T, dt)
        self.apo_altitude = VesselStreams.Orbit.apoapsisAltitudeStream()
        self.mass = VesselStreams.mass()
        self.orbit_radius = VesselStreams.Orbit.radiusStream()
        self.available_thrust = VesselStreams.availableThrust()

        # Activate engines
        vessel.control.activate_next_stage()

    def update(self, T, dt):

        if self.apo_altitude() > self.target_altitude:
            target_twr = 0
        else:
            target_twr = 0.2 + self.pid.update(self.apo_altitude() / self.target_altitude, dt)

        g = gravitationalAcceleration(self.GM, self.orbit_radius())
        throttle = throttleFromTwr(target_twr, self.mass(), self.available_thrust(), g)

        vessel.control.throttle = throttle

        return super().update(T, dt)

    def provideTelemetry(self):
        data = TelemetryBuilder(self.getName())
        data.addData('target', self.target_altitude)
        data.addData('apo_altitude', self.apo_altitude())
        return data.build()

    def onExit(self, T, dt):
        super().onExit(T, dt)
        vessel.control.throttle = 0

        # Close streams
        self.apo_altitude.remove()
        self.mass.remove()
        self.orbit_radius.remove()
        self.available_thrust.remove()


class DescendingState(StateBase):
    def __init__(self):
        super().__init__("descending", [LandingEvent(StateMachine.TERMINATE_MACHINE)])

        self.altitude = None

    def onEntry(self, T, dt):
        super().onEntry(T, dt)
        self.altitude = VesselStreams.Flight.surfaceAltitudeStream()

    def update(self, T, dt):
        return super().update(T, dt)

    def provideTelemetry(self):
        data = TelemetryBuilder(self.getName())
        data.addData('altitude', self.altitude())
        return data.build()

    def onExit(self, T, dt):
        super().onExit(T, dt)
        self.altitude.remove()


GrasshopperStates = {
    GrasshopperStatesEnum.AwaitLiftoff: CountdownState(),
    GrasshopperStatesEnum.Powering: AscendingState(100),
    GrasshopperStatesEnum.Descending: DescendingState()
    }

