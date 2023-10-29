from random import randrange
from parameters import *
from station_status import StationStatus
from vcs_status import VCSStatus

def csmaCA(stationA, stationB, is_hidden_terminals, is_vcs_enabled):

    current_slot = 0
    temp_counter = 0

    # Modify how the stations should operate depending on topology and whether vcs is enabled
    stationA.is_hidden_terminals = is_hidden_terminals
    stationA.is_vcs_enabled = is_vcs_enabled
    stationB.is_hidden_terminals = is_hidden_terminals
    stationB.is_vcs_enabled = is_vcs_enabled

    # Figure out which station starts first
    if (stationA.frames[stationA.frame_index] < stationB.frames[stationB.frame_index]):
        current_slot = stationA.frames[stationA.frame_index]
    else:
        current_slot = stationB.frames[stationB.frame_index]

    while(current_slot < MAX_SIMULATION_SLOTS and (stationA.status != StationStatus.DONE or stationB.status != StationStatus.DONE)):
        
        # If a station is free, check if they have a frame to send
        if (stationA.status == StationStatus.FREE and stationA.frames[stationA.frame_index] <= current_slot):
            stationA.switch_to_status(StationStatus.SENSING)
        if (stationB.status == StationStatus.FREE and stationB.frames[stationB.frame_index] <= current_slot):
            stationB.switch_to_status(StationStatus.SENSING)

        # "Move forward a slot" and check what A and B should do
        stationA.update_counters()
        stationB.update_counters()
        current_slot += 1

        # Switch states for A and B depending on status and counter values
        stationA.update_status()
        stationB.update_status()

        # Check if A and/or B try to start transmitting
        if (stationA.is_xmitting() and stationB.is_xmitting()):
            # Move current_slot past collision slots to "skip" the collision
            if (stationA.counter < stationB.counter):
                temp_counter = stationA.counter
                current_slot += temp_counter
                stationB.skip_counter(temp_counter)
                stationA.skip_counter(temp_counter)
            else:
                temp_counter = stationB.counter
                current_slot += temp_counter
                stationA.skip_counter(temp_counter)
                stationB.skip_counter(temp_counter)

            # Mark the current transmission as a collision for each station
            stationA.collision_flag = True
            stationB.collision_flag = True
            stationA.update_status()
            stationB.update_status()
        else:
            if (is_hidden_terminals and is_ap_sending_ack([stationA, stationB])):
                # For special case in hidden terminals when frame is sent during ack
                if (stationA.status == StationStatus.SENDING or stationA.status == StationStatus.SENDING_RTS):
                    stationA.collision_flag = True
                if (stationB.status == StationStatus.SENDING or stationB.status == StationStatus.SENDING_RTS):
                    stationB.collision_flag = True
            elif (is_hidden_terminals and is_ap_sending_cts([stationA, stationB])):
                # For special case when one station send RTS right as AP sends CTS
                if (stationA.vcs_status == VCSStatus.CLEAR_TO_SEND):
                    if (stationB.status == StationStatus.SENDING_RTS):
                        stationB.collision_flag = True
                        stationB.missed_cts_flag = True
                    else:
                        stationB.missed_cts_flag = False
                        if (stationB.status != StationStatus.WAITING_FOR_NAV):
                            stationB.switch_to_status(StationStatus.WAITING_FOR_NAV)
                elif (stationB.vcs_status == VCSStatus.CLEAR_TO_SEND):
                    if (stationA.status == StationStatus.SENDING_RTS):
                        stationA.collision_flag = True
                        stationA.missed_cts_flag = True 
                    else:
                        stationA.missed_cts_flag = False
                        if (stationA.status != StationStatus.WAITING_FOR_NAV):
                            stationA.switch_to_status(StationStatus.WAITING_FOR_NAV)
            elif (is_vcs_enabled or not is_hidden_terminals):
                if (stationA.is_reserving_channel() and not stationB.missed_cts_flag):
                    if (stationB.status != StationStatus.WAITING_FOR_NAV):
                        stationB.switch_to_status(StationStatus.WAITING_FOR_NAV)

                    # At this point, A and B will not collide, so we skip forward until A's status changes
                    temp_counter = stationA.counter
                    current_slot += temp_counter
                    stationB.skip_counter(temp_counter)
                    stationB.update_status()
                    stationA.skip_counter(temp_counter)
                    stationA.update_status()
                elif (stationB.is_reserving_channel() and not stationA.missed_cts_flag):
                    if (stationA.status != StationStatus.WAITING_FOR_NAV):
                        stationA.switch_to_status(StationStatus.WAITING_FOR_NAV)

                    # At this point, A and B will not collide, so we skip forward until B's status changes
                    temp_counter = stationB.counter
                    current_slot += temp_counter
                    stationA.skip_counter(temp_counter)
                    stationA.update_status()
                    stationB.skip_counter(temp_counter)
                    stationB.update_status()

'''
Check if the ap is sending an ack. Used during Hidden Terminals special case.
'''
def is_ap_sending_ack(stations):
    if (any([s.status == StationStatus.WAITING_FOR_ACK and s.collision_flag == False for s in stations])):
        return True
    return False

'''
Check if the ap is sending cts. Used during Hidden Terminals VCS special case.
'''
def is_ap_sending_cts(stations):
    if (any([s.status == StationStatus.WAITING_FOR_CTS and s.collision_flag == False for s in stations])):
        return True
    return False