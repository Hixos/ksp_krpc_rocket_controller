import time

from global_streams import global_streams
from fsm.fsm import StateMachine
from ksp_krpc import Stream

from telemetry.telemetry import update as updateTelemetry, TelemetryProviderInterface, TelemetryBuilder, addProvider, \
    addUser
from telemetry.live_display import live_telemetry

from controllers.grasshopper import GrasshopperStates, AscendingState, DescendingState

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
    TELEMETRY_GKEY = "main"

    def getProviderKey(self):
        return "main"

    def provideTelemetry(self):
        builder = TelemetryBuilder("main", "Main Telemetry")
        builder.addData('t', "T", T, "s")
        builder.addData('game_dt', "Game dt", game_dt, "s")
        builder.addData('active_state', "Current state", machine.getActiveState().getName())
        return builder.build()


addProvider(MainTelemetryProvider())
addProvider(machine)

live_telemetry.logGroup(MainTelemetryProvider.TELEMETRY_GKEY)
live_telemetry.logGroup(AscendingState.TELEMETRY_GKEY)
live_telemetry.logGroup(DescendingState.TELEMETRY_GKEY)

live_telemetry.showWindow()

addUser(live_telemetry)

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
            updateTelemetry()
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

# Check for leaks
print("\nScript ended")
if len(Stream.streams) > 0:
    print("\n\nUNCLOSED STREAMS:")
    for k in Stream.streams.keys():
        print("{} - instances: {}".format(k, Stream.streams[k].open_instances))

# Wait for user to close telemetry window
live_telemetry.startMainLoop()
