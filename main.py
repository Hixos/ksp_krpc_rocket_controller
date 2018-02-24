import time

from global_streams import global_streams
from fsm.fsm import StateMachine
from ksp_krpc import Stream

from telemetry.telemetry import update as updateTelemetry, TelemetryProviderInterface, TelemetryBuilder, addProvider

from controllers.grasshopper import GrasshopperStates


# Interval of time between loops of the main loop
loop_dt = 0.1

# Interval of in-game time elapsed between loops
game_dt = 0

# Epoch
T0 = global_streams.ut()

T = 0
last_T = 0

time.sleep(loop_dt)


class MainTelemetryProvider(TelemetryProviderInterface):
    def getProviderKey(self):
        return "main"

    def provideTelemetry(self):
        builder = TelemetryBuilder("main")
        builder.addData('T0', T0)
        builder.addData('T', T)
        builder.addData('game_dt', game_dt)
        return builder.build()


machine = StateMachine(GrasshopperStates)

addProvider(MainTelemetryProvider())
addProvider(machine)

while True:
    start = time.time()
    if not global_streams.game_paused():  # If game is paused, pause too
        T = global_streams.ut() - T0  # Game time elapsed from start of the program
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
