from .grasshopper_states import *

from telemetry.telemetry import telemetry_manager
from telemetry.live_display import live_telemetry
from telemetry.logger import telemetry_logger
from fsm.fsm import StateMachine
from enum import IntEnum, unique


@unique
class GrasshopperStatesEnum(IntEnum):
    AwaitLiftoff = 1
    Powering = 2
    Descending = 3

countdown = CountdownState(GrasshopperStatesEnum.Powering, countdown_length=3)
ascending = AscendingState(GrasshopperStatesEnum.Descending, target_altitude=1000)
descending = DescendingState(StateMachine.TERMINATE_MACHINE)

GrasshopperStates = {
    GrasshopperStatesEnum.AwaitLiftoff: countdown,

    GrasshopperStatesEnum.Powering: ascending,

    GrasshopperStatesEnum.Descending: descending
    }

telemetry_manager.registerProvider('ascending_state', "Ascending State", ascending)
telemetry_manager.registerProvider('descending_state', "Descending State", descending)

live_telemetry.displayProvider('ascending_state')
telemetry_logger.logProvider('ascending_state')
#live_telemetry.displayProvider('descending_state')
