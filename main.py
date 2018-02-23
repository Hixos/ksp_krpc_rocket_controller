import time

from global_streams import global_streams
from fsm.fsm import StateMachine

from telemetry.telemetry import update as updateTelemetry

from controllers.grasshopper import GrasshopperStates

dt = 0.1
game_dt = 0

T0 = global_streams.ut()
last_T = 0


# From universal game time to relative time from the start of the script
def TfromUT(t_ut): return t_ut - T0

time.sleep(dt)
machine = StateMachine(GrasshopperStates)

while True:
    start = time.time()
    if not global_streams.game_paused():  # If game is paused, pause too
        T = TfromUT(global_streams.ut())  # Game time elapsed from start of the program
        game_dt = T - last_T

        # Flight reverted, quicksave loaded or other invalidating actions. Stop the script.
        if game_dt < 0:
            print("In-game discontinuity detected. Stopping script")
            break

        # Don't control anything if game_dt is zero
        if game_dt > 0:
            go_on = machine.update(T, game_dt)
            updateTelemetry(machine)
            if not go_on:
                break

        last_T = T
    end = time.time()

    # Sleep for the remaining time in the slot
    time.sleep(max(max(dt/(1+global_streams.physics_warp()), 0.02) - end + start, 0))


global_streams.global_streams.closeStreams()

print("\nScript ended")
if len(global_streams.Stream.streams) > 0:
    print("\n\nUNCLOSED STREAMS:")
    for k in global_streams.Stream.streams.keys():
        print("{} - instances: {}".format(k, global_streams.Stream.streams[k].open_instances))
