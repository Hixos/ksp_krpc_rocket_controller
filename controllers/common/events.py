from fsm.fsm import StateMachine, EventBase
from ksp_krpc import vessel, VesselStreams
from utils.vessel_utils import lowest_altitude

# Copy this when creating new events
class EmptyEvent(EventBase):
    def __init__(self):
        super().__init__("EMPTY_EVENT")

    def onEntry(self, T, dt):
        super().onEntry(T, dt)

    def check(self, T, dt):
        return StateMachine.NO_EVENT

    def onExit(self, T, dt):
        super().onExit(T, dt)


class LiftoffEvent(EventBase):
    def __init__(self, countdown_length, next_state_id):
        super().__init__("LIFTOFF_EVENT")
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
            return StateMachine.NO_EVENT


class LandingEvent(EventBase):
    def __init__(self, next_state_id):
        super().__init__("EMPTY EVENT")
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

        return StateMachine.NO_EVENT

    def onExit(self, T, dt):
        super().onExit(T, dt)
        self.altitude.remove()
        self.bounding_box.remove()
