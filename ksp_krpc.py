import krpc

conn = krpc.connect(name="Rocket Controller")

ut = conn.add_stream(getattr, conn.space_center, 'ut')
physics_warp = conn.add_stream(getattr, conn.space_center, 'physics_warp_factor')
rails_warp = conn.add_stream(getattr, conn.space_center, 'rails_warp_factor')

vessel = conn.space_center.active_vessel


class VesselStreams:
    @staticmethod
    def boundingBoxStream(reference_frame): return conn.add_stream(vessel.bounding_box, reference_frame)

    @staticmethod
    def availableThrust(): return conn.add_stream(getattr, vessel, 'available_thrust')

    @staticmethod
    def mass(): return conn.add_stream(getattr, vessel, 'mass')

    class Flight:
        @staticmethod
        def surfaceAltitudeStream(): return conn.add_stream(getattr, vessel.flight(), 'surface_altitude')

        @staticmethod
        def meanAltitudeStream(): return conn.add_stream(getattr, vessel.flight(), 'mean_altitude')

    class Orbit:
        @staticmethod
        def apoapsisAltitudeStream(): return conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')

        @staticmethod
        def radiusStream(): return conn.add_stream(getattr, vessel.orbit, 'radius')

        class CelestialBody:
            @staticmethod
            def gravitationalParameter(): return vessel.orbit.body.gravitational_parameter
