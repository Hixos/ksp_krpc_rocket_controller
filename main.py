import time
import ksp_krpc
from fsm.fsm import StateMachine
from controllers.grasshopper import GrasshopperStates

dt = 0.1
game_dt = 0

T0 = ksp_krpc.ut()
last_T = 0


# From universal game time to relative time from the start of the script
def TfromUT(t_ut): return t_ut - T0


time.sleep(dt)
machine = StateMachine(GrasshopperStates, 0, 0)

while True:
    start = time.time()
    if not ksp_krpc.game_paused():  # If game is paused, pause too
        T = TfromUT(ksp_krpc.ut())  # Game time elapsed from start of the program
        game_dt = T - last_T

        # Flight reverted, quicksave loaded or other invalidating actions. Stop the script.
        if game_dt < 0:
            print("In-game discontinuity detected. Stopping script")
            break

        # Don't control anything if game_dt is zero
        if game_dt > 0:
            if not machine.update(T, game_dt):
                break

        last_T = T
    end = time.time()

    # Sleep for the remaining time in the slot
    time.sleep(max(max(dt/(1+ksp_krpc.physics_warp()), 0.02) - end + start, 0))


ksp_krpc.closeGlobalStreams()

print("\nScript ended")
if len(ksp_krpc.Stream.streams) > 0:
    print("\n\nUNCLOSED STREAMS:")
    for k in ksp_krpc.Stream.streams.keys():
        print("{} - instances: {}".format(k, ksp_krpc.Stream.streams[k].open_instances))
