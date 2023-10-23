from random import randrange
from parameters import *
from station import Station
from station_status import StationStatus

def csmaCA(stationA, stationB, is_hidden_terminals, is_vcs):

    currentSlot = 0

    # Figure out which station starts first
    if (stationA.frames[stationA.frame_index] < stationB.frames[stationB.frame_index]):
        currentSlot = stationA.frames[stationA.frame_index]
    else:
        currentSlot = stationB.frames[stationB.frame_index]

    while(currentSlot < MAX_SIMULATION_SLOTS and (stationA.status != StationStatus.DONE or stationB.status != StationStatus.DONE)):
        
        # If a station is free, check if they have a frame to send
        if (stationA.status == StationStatus.FREE and stationA.frames[stationA.frame_index] <= currentSlot):
            print("Station A found a frame: " + str(stationA.frames[stationA.frame_index]))
            print("Current slot: " + str(currentSlot) + '\n')
            stationA.switch_to_status(StationStatus.SENSING)
        if (stationB.status == StationStatus.FREE and stationB.frames[stationB.frame_index] <= currentSlot):
            print("Station B found a frame: " + str(stationB.frames[stationB.frame_index]))
            print("Current slot: " + str(currentSlot) + '\n')
            stationB.switch_to_status(StationStatus.SENSING)

        # "Move forward a slot" and check what A and B should do
        stationA.update_counters()
        stationB.update_counters()
        currentSlot += 1

        # Switch states for A and B depending on status and counter values
        stationA.update_status()
        stationB.update_status()

        # Check if A and/or B try to start transmitting
        if (stationA.is_xmitting() and stationB.is_xmitting()):
            # Move currentSlot past collision slots to "skip" the collision
            if (stationA.counter < stationB.counter):
                currentSlot += stationA.counter
                stationB.skip_counter(stationA.counter)
                stationA.skip_counter(stationA.counter)
            else:
                currentSlot += stationB.counter
                stationA.skip_counter(stationB.counter)
                stationB.skip_counter(stationB.counter)

            # Mark the current transmission as a collision for each station
            stationA.collision_flag = True
            stationB.collision_flag = True
            stationA.update_status()
            stationB.update_status()
        elif (is_hidden_terminals and is_ap_sending_ack([stationA, stationB])):
            # For special case in hidden terminals when frame is sent during ack
            if (stationA.status == StationStatus.SENDING):
                stationA.frame_sent_while_busy_flag = True
            elif (stationB.status == StationStatus.SENDING):
                stationB.frame_sent_while_busy_flag = True
        elif (not is_hidden_terminals):
            if (stationA.status == StationStatus.SENDING):
                stationB.switch_to_status(StationStatus.WAITING_FOR_NAV)

                # "Skip" ahead to the end of A's transmission
                currentSlot += stationA.counter
                stationB.skip_counter(stationA.counter)
                stationB.update_status()
                stationA.skip_counter(stationA.counter)
                stationA.update_status()
            elif (stationB.status == StationStatus.SENDING):
                stationA.switch_to_status(StationStatus.WAITING_FOR_NAV)

                # "Skip" ahead to the end of B's transmission
                currentSlot += stationB.counter
                stationA.skip_counter(stationB.counter)
                stationA.update_status()
                stationB.skip_counter(stationB.counter)
                stationB.update_status()

'''
Check if the ap is sending an ack. Used during Hidden Terminals special case.
'''
def is_ap_sending_ack(stations):
    if (any([s.status == StationStatus.WAITING_FOR_ACK and s.collision_flag == False for s in stations])):
        return True
    return False