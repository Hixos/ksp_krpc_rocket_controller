
def lowest_altitude(surface_altitude, bounding_box):
    """
    Altitude over terraing of the lowest point of the vessel. Should be 0 when on the ground
    :param surface_altitude: Altitude of CoM over the surface
    :param bounding_box: Vessel bound box, in surface_reference_frame
    :return: Altitude in meters
    """
    return surface_altitude + bounding_box[0][0]


def throttleFromTwr(twr, mass, available_thrust, g):
    """
    Returns the throttle setting to obtain the specified TWR
    :param twr:
    :param mass:
    :param available_thrust:
    :param g:
    :return: throttle setting in [0, 1]
    """
    return min(max(twr*mass*g/available_thrust, 0), 1)
