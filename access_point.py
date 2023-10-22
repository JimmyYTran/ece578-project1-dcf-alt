from random import randrange
from parameters import *

def csmaCA(arrivalsA, arrivalsB):
    successesA = 0
    successesB = 0
    collisions = 0

    i = 0               # Index for arrivals from A
    j = 0               # Index for arrivals from B
    currentSlot = 0
    cwA = DEFAULT_CW
    cwB = DEFAULT_CW
    difsA = DIFS
    difsB = DIFS
    backoffA = 0
    backoffB = 0
    isSensingA = False  # Is station A sensing the channel?
    isSensingB = False  # Is station B sensing the channel?

    # Figure out which station starts first
    if (arrivalsA[i] < arrivalsB[j]):
        currentSlot = arrivalsA[i]
    else:
        currentSlot = arrivalsB[j]

    while(currentSlot < MAX_SIMULATION_SLOTS and (i < len(arrivalsA) or j < len(arrivalsB))):
        
        # If a station is not currently sensing, check if they have a frame to send
        if (not isSensingA and arrivalsA[i] <= currentSlot):
            isSensingA = True
            backoffA = randrange(cwA)
        if (not isSensingB and arrivalsB[j] <= currentSlot):
            isSensingB = True
            backoffB = randrange(cwB)

        if (isSensingA):
            # Wait for difs slots. After waiting difs slots, decrement backoff counter
            if (difsA > 0):
                difsA = difsA - 1
            elif (backoffA > 0):
                backoffA = backoffA - 1

            # Check if A is ready to attempt transmission
            if (difsA == 0 and backoffA == 0):
                isSensingA = False

        if (isSensingB):
            # Wait for difs slots. After waiting difs slots, decrement backoff counter
            if (difsB > 0):
                difsB = difsB - 1
            elif (backoffB > 0):
                backoffB = backoffB - 1

            # Check if B is ready to attempt transmission
            if (difsB == 0 and backoffB == 0):
                isSensingB = False

        # Move forward a slot (either A or B is sensing, or nothing happened)
        currentSlot += 1

        if (difsA == 0 and backoffA == 0 and difsB == 0 and backoffB == 0):
            # If backoffs match, then there is a collision
            currentSlot += FRAME_SIZE_IN_SLOTS + SIFS + ACK

            # Make sure we haven't exceeded simulation time
            if (currentSlot < MAX_SIMULATION_SLOTS):
                collisions += 1

                # Reset DIFS counter for both A and B
                difsA = DIFS
                difsB = DIFS

                # Double contention windows for both A and B
                if (cwA < CW_MAX):
                    cwA = cwA * 2
                if (cwB < CW_MAX):
                    cwB = cwB * 2
        elif (difsA == 0 and backoffA == 0):
            # Only A gets to transmit and the channel is reserved until then
            currentSlot += FRAME_SIZE_IN_SLOTS + SIFS + ACK

            # Make sure we haven't exceeded simulation time
            if (currentSlot < MAX_SIMULATION_SLOTS):
                successesA += 1
                i += 1

                # Reset both DIFS counters (in case DIFS period for B was interrupted)
                difsA = DIFS
                difsB = DIFS

                # Reset contention window for A
                cwA = DEFAULT_CW
        elif (difsB == 0 and backoffB == 0):
            # Only B gets to transmit and the channel is reserved until then
            currentSlot += FRAME_SIZE_IN_SLOTS + SIFS + ACK

            # Make sure we haven't exceeded simulation time
            if (currentSlot < MAX_SIMULATION_SLOTS):
                successesB += 1
                j += 1

                # Reset both DIFS counters (in case DIFS period for A was interrupted)
                difsA = DIFS
                difsB = DIFS

                # Reset contention window for B
                cwB = DEFAULT_CW
        
        # If a station has no more arrivals, ignore that station during simulation
        if (i >= len(arrivalsA)):
            isSensingA = True
            difsA = -1
            backoffA = -1
        if (j >= len(arrivalsB)):
            isSensingB = True
            difsB = -1
            backoffB = -1
            
    return successesA, successesB, collisions
