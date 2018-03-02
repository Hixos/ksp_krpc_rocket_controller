from fsm.fsm import StateMachine, EventBase
from ksp_krpc import vessel, VesselStreams
from utils.vessel_utils import lowest_altitude


# Copy this when creating new events
class EmptyEvent(EventBase):
    def __init__(self, event_name):
        super().__init__(event_name)

    def onEntry(self, T, dt):
        super().onEntry(T, dt)

    def check(self, T, dt):
        return StateMachine.NO_STATE

    def onExit(self, T, dt):
        super().onExit(T, dt)


class LiftoffEvent(EventBase):
    def __init__(self, countdown_length, next_state_id, event_name="On Liftoff"):
        super().__init__(event_name)
        self.T0 = 0
        self.countdown_length = countdown_length
        self.next_state_id = next_state_id

    def onEntry(self, T, dt):
        super().onEntry(T, dt)
        self.T0 = T + self.countdown_length
        print("T0 at: {}".format(self.T0))

    def check(self, T, dt):
        if T > self.T0:
            return self.next_state_id
        else:
            return StateMachine.NO_STATE


class AtApoapsisEvent(EventBase):
    def __init__(self, next_state_id, start_after_seconds=0, target_apoapsis=0, tolerance=0.01,
                 event_name="At Apoapsis"):
        super().__init__(event_name)

        self.next_state_id = next_state_id
        self.tolerance = tolerance
        self.start_after_seconds = start_after_seconds
        self.target_apoapsis = target_apoapsis

        if target_apoapsis > 0:
            self.has_target = True
        else:
            self.has_target = False

        self.T0 = 0

        self.apoapsis = None
        self.altitude = None
        self.vertical_speed = None

    def onEntry(self, T, dt):
        self.T0 = T

        self.altitude = VesselStreams.Flight.meanAltitudeStream()
        self.apoapsis = VesselStreams.Orbit.apoapsisAltitudeStream()
        self.vertical_speed = VesselStreams.Flight.verticalSpeed()

    def check(self, T, dt):
        if self.has_target:
            apo = self.target_apoapsis
        else:
            apo = self.apoapsis()

        if abs(apo - self.altitude())/self.apoapsis() < self.tolerance\
                and T > self.T0 + self.start_after_seconds and self.vertical_speed() < 0:
            return self.next_state_id

        return StateMachine.NO_STATE

    def onExit(self, T, dt):
        self.altitude.remove()
        self.apoapsis.remove()
        self.vertical_speed.remove()


class LandingEvent(EventBase):
    def __init__(self, next_state_id, event_name="On Landing"):
        super().__init__(event_name)
        self.next_state_id = next_state_id
        self.altitude = None
        self.bounding_box = None

    def onEntry(self, T, dt):
        super().onEntry(T, dt)
        self.altitude = VesselStreams.Flight.surfaceAltitudeStream()
        self.bounding_box = VesselStreams.boundingBoxStream(vessel.surface_reference_frame)

    def check(self, T, dt):
        if lowest_altitude(self.altitude(), self.bounding_box()) <= 0:
            return self.next_state_id

        return StateMachine.NO_STATE

    def onExit(self, T, dt):
        super().onExit(T, dt)
        self.altitude.remove()
        self.bounding_box.remove()
