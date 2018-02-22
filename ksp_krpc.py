import krpc

conn = krpc.connect(name="Rocket Controller")

ut = conn.add_stream(getattr, conn.space_center, 'ut')
physics_warp = conn.add_stream(getattr, conn.space_center, 'physics_warp_factor')
rails_warp = conn.add_stream(getattr, conn.space_center, 'rails_warp_factor')

vessel = conn.space_center.active_vessel


class VesselStreams:
    @staticmethod
    def surfaceAltitudeStream(): return conn.add_stream(getattr, vessel.flight(), 'surface_altitude')

    @staticmethod
    def boundingBoxStream(reference_frame): return conn.add_stream(vessel.bounding_box, vessel.surface_reference_frame)
