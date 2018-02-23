import krpc

conn = krpc.connect(name="Rocket Controller")

ut = conn.add_stream(getattr, conn.space_center, 'ut')
physics_warp = conn.add_stream(getattr, conn.space_center, 'physics_warp_factor')
rails_warp = conn.add_stream(getattr, conn.space_center, 'rails_warp_factor')

vessel = conn.space_center.active_vessel


class Stream:
    """
    krpc.stream.Stream wrapper to allow simultaneous use of the same stream in multiple places
    Keeps track of how many times a stream has been requested and closes it only when no one is using it anymore
    """
    streams = {}

    def __init__(self, name, stream_params):
        self.krpc_stream = conn.add_stream(*stream_params)
        self.open_instances = 1
        self.name = name

    def __call__(self):
        return self.krpc_stream()

    def remove(self):
        self.open_instances -= 1
        print("{} remaining instances: {}".format(self.name, self.open_instances))
        if self.open_instances == 0:
            self.krpc_stream.remove()
            del Stream.streams[self.name]

    @staticmethod
    def getStream(name, stream_params):
        if name in Stream.streams:
            s = Stream.streams[name]  # type: Stream
            s.open_instances += 1
            return s
        else:
            s = Stream(name, stream_params)
            Stream.streams[name] = s
            return s


class VesselStreams:
    @staticmethod
    def boundingBoxStream(reference_frame): return Stream.getStream('vessel.bounding_box', (vessel.bounding_box, reference_frame))

    @staticmethod
    def availableThrust():
        return Stream.getStream('vessel.available_thrust', (getattr, vessel, 'available_thrust'))

    @staticmethod
    def mass():
        return Stream.getStream('vessel.mass', (getattr, vessel, 'mass'))

    class Flight:
        @staticmethod
        def surfaceAltitudeStream():
            return Stream.getStream('vessel.flight.surface_altitude', (getattr,  vessel.flight(), 'surface_altitude'))

        @staticmethod
        def meanAltitudeStream():
            return Stream.getStream('vessel.flight.mean_altitude', (getattr, vessel.flight(), 'mean_altitude'))

    class Orbit:
        @staticmethod
        def apoapsisAltitudeStream():
            return Stream.getStream('vessel.orbit.apoapsis_altitude', (getattr, vessel.orbit, 'apoapsis_altitude'))

        @staticmethod
        def radiusStream():
            return Stream.getStream('vessel.orbit.radius', (getattr, vessel.orbit, 'radius'))

        class CelestialBody:
            @staticmethod
            def gravitationalParameter(): return vessel.orbit.body.gravitational_parameter





