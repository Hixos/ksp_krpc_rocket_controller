from .grasshopper_states import *
from fsm.fsm import StateMachine
from enum import IntEnum, unique


@unique
class GrasshopperStatesEnum(IntEnum):
    AwaitLiftoff = 1
    Powering = 2
    Descending = 3


GrasshopperStates = {
    GrasshopperStatesEnum.AwaitLiftoff: CountdownState(GrasshopperStatesEnum.Powering,
                                                       countdown_length=3),

    GrasshopperStatesEnum.Powering: AscendingState(GrasshopperStatesEnum.Descending,
                                                   target_altitude=1000),

    GrasshopperStatesEnum.Descending: DescendingState(StateMachine.TERMINATE_MACHINE)
    }
