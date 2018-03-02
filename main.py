import time

from global_streams import global_streams
from fsm.fsm import StateMachine
from ksp_krpc import Stream, VesselStreams

from telemetry.telemetry import telemetry_manager as tm_manager, TelemetryProviderInterface, TelemetryDescriptionBuilder

from telemetry.live_display import live_telemetry
from telemetry.logger import telemetry_logger

from controllers.grasshopper.grasshopper import GrasshopperStates

# Interval of time between loops of the main loop
loop_dt = 0.1

# Interval of in-game time elapsed between loops
game_dt = 0

epoch = global_streams.ut()

# In-game time since epoch
T = 0
last_T = 0

time.sleep(loop_dt)

machine = StateMachine(GrasshopperStates)


class MainTelemetryProvider(TelemetryProviderInterface):
    def __init__(self):
        self.mean_altitude = VesselStreams.Flight.meanAltitudeStream()
        self.surf_altitude = VesselStreams.Flight.surfaceAltitudeStream()
        self.apo_altitude = VesselStreams.Orbit.apoapsisAltitudeStream()

    def getTelemetry(self):
        return [game_dt, machine.getActiveState().getName(), self.surf_altitude(),
                self.mean_altitude(), self.apo_altitude()]

    def describeTelemetry(self):
        return TelemetryDescriptionBuilder()\
            .addData('game_dt', 'Game dt', 's')\
            .addData('active_state', 'Active State')\
            .addData('surface_altitude', "Surface Altitude", 'm') \
            .addData('mean_altitude', "Mean Altitude", 'm') \
            .addData('apo_altitude', 'Apoapsis Altitude', 'm')\
            .build()

    def close(self):
        self.mean_altitude.remove()
        self.apo_altitude.remove()
        self.surf_altitude.remove()

main_provider = MainTelemetryProvider()
tm_manager.registerProvider('main_telemetry', "Main Telemetry", main_provider)

live_telemetry.displayProvider('main_telemetry')
live_telemetry.showWindow()

telemetry_logger.logProvider('main_telemetry')

tm_manager.registerUser("live_display", live_telemetry)
tm_manager.registerUser("logger", telemetry_logger)

while True:
    start = time.time()
    if not global_streams.game_paused():  # If game is paused, pause too
        T = global_streams.ut() - epoch  # Game time elapsed from start of the program
        game_dt = T - last_T

        # Flight reverted, quicksave loaded or other invalidating actions. Stop the script.
        if game_dt < 0:
            print("In-game time discontinuity detected. Stopping script")
            break

        # Don't control anything if game_dt is zero
        if game_dt > 0:
            go_on = machine.update(T, game_dt)
            tm_manager.update(T, game_dt)
            if not go_on:
                machine.terminate(T, game_dt)
                print("State machine terminated")
                break

        last_T = T
    end = time.time()

    # Sleep for the remaining time in the slot
    time.sleep(max(max(loop_dt / (1 + global_streams.physics_warp()), 0.02) - end + start, 0))


# Cleanup
global_streams.closeStreams()
main_provider.close()

# Check for leaks
print("\nScript ended")
if len(Stream.streams) > 0:
    print("\n\nUNCLOSED STREAMS:")
    for k in Stream.streams.keys():
        print("{} - instances: {}".format(k, Stream.streams[k].open_instances))

# Wait for user to close telemetry window
live_telemetry.startMainLoop()
