import numpy as np
from station_status import StationStatus
from vcs_status import VCSStatus
from parameters import *

class Station:

    def __init__(self, name, lam):
        self.successes = 0
        self.collisions = 0
        self.curr_CW = DEFAULT_CW
        self.counter = DIFS
        self.backoff = 0
        self.name = name
        self.frames = []
        self.frame_index = 0
        self.status = StationStatus.FREE
        self.lam = lam

        self.is_hidden_terminals = False
        self.is_vcs_enabled = False
        self.collision_flag = False
        self.missed_cts_flag = False
        self.vcs_status = VCSStatus.NONE

        running_sum = 0
        avg_slot_arrival = (1/self.lam)/SLOT_DURATION
        while running_sum < MAX_SIMULATION_SLOTS:
            running_sum += np.random.poisson(lam=avg_slot_arrival)
            self.frames.append(running_sum)

    '''
    Update the status of the station to new_status, and reset counters as needed.
    The station's possible statuses may change depending on the channel topology and whether vcs is enabled.
    '''
    def switch_to_status(self, new_status):
        if (self.status != StationStatus.DONE):
            self.status = new_status

            if new_status == StationStatus.SENSING:
                self.counter = DIFS
            elif new_status == StationStatus.WAITING_FOR_NAV:
                if self.is_hidden_terminals and self.is_vcs_enabled:
                    self.counter = CTS + SIFS + FRAME_SIZE_IN_SLOTS + SIFS + ACK
                elif self.is_vcs_enabled:
                    self.counter = RTS + SIFS + CTS + SIFS + FRAME_SIZE_IN_SLOTS + SIFS + ACK
                else:
                    self.counter = FRAME_SIZE_IN_SLOTS + SIFS + ACK
            elif new_status == StationStatus.BACKOFF:
                # Generate a new backoff unless still counting down from a previous contention period
                if self.backoff == 0:
                    # numpy's randint -> Return random integers from low (inclusive) to high (exclusive).
                    self.backoff = np.random.randint(0, self.curr_CW)
                    if self.backoff == 0:
                        if self.is_vcs_enabled:
                            self.vcs_status = VCSStatus.REQUEST_TO_SEND
                            self.status = StationStatus.SENDING_RTS
                            self.counter = RTS
                        else:
                            self.status = StationStatus.SENDING
                            self.counter = FRAME_SIZE_IN_SLOTS
            elif new_status == StationStatus.SENDING_RTS:
                self.counter = RTS
            elif new_status == StationStatus.WAITING_FOR_CTS:
                self.counter = CTS
            elif new_status == StationStatus.SENDING:
                self.counter = FRAME_SIZE_IN_SLOTS
            elif new_status == StationStatus.WAITING_FOR_SIFS:
                self.counter = SIFS
            elif new_status == StationStatus.WAITING_FOR_ACK:
                self.counter = ACK

    '''
    Decrements the station's counters based on its state (moves forward a slot).
    This should be run simultaneously with A and B so that both stations stay aligned in time.
    Make sure that the access point counter also moves forward a slot.
    '''
    def update_counters(self):
        if self.status == StationStatus.BACKOFF:
            self.backoff -= 1
        elif self.status != StationStatus.FREE and self.status != StationStatus.DONE:
            self.counter -= 1

    '''
    Determines which status the station will be in next and updates the status.
    '''
    def update_status(self):
        if self.status == StationStatus.SENSING:
            if self.counter == 0:
                self.switch_to_status(StationStatus.BACKOFF)
        elif self.status == StationStatus.WAITING_FOR_NAV:
            if self.counter == 0:
                self.switch_to_status(StationStatus.FREE)
        elif self.status == StationStatus.BACKOFF:
            if self.backoff == 0:
                if self.is_vcs_enabled:
                    self.vcs_status = VCSStatus.REQUEST_TO_SEND
                    self.switch_to_status(StationStatus.SENDING_RTS)
                else:
                    self.switch_to_status(StationStatus.SENDING)
        elif self.status == StationStatus.SENDING_RTS:
            if self.counter == 0:
                self.switch_to_status(StationStatus.WAITING_FOR_SIFS)
        elif self.status == StationStatus.WAITING_FOR_CTS:
            if self.counter == 0:
                if self.vcs_status == VCSStatus.CLEAR_TO_SEND:
                    self.switch_to_status(StationStatus.WAITING_FOR_SIFS)
                else:
                    self.vcs_status = VCSStatus.NONE
                    self.update_on_collision()
        elif self.status == StationStatus.SENDING:
            if self.counter == 0:
                if self.is_vcs_enabled:
                    self.vcs_status = VCSStatus.NONE
                self.switch_to_status(StationStatus.WAITING_FOR_SIFS)
        elif self.status == StationStatus.WAITING_FOR_SIFS:
            if self.counter == 0:
                if not self.is_vcs_enabled or self.vcs_status == VCSStatus.NONE:
                    self.switch_to_status(StationStatus.WAITING_FOR_ACK)
                else:
                    if self.vcs_status == VCSStatus.REQUEST_TO_SEND:
                        if not self.collision_flag:
                            self.vcs_status = VCSStatus.CLEAR_TO_SEND
                        else:
                            self.vcs_status = VCSStatus.NO_AP_RESPONSE
                        self.switch_to_status(StationStatus.WAITING_FOR_CTS)
                    elif self.vcs_status == VCSStatus.CLEAR_TO_SEND:
                        self.switch_to_status(StationStatus.SENDING)               
        elif self.status == StationStatus.WAITING_FOR_ACK:
            if self.counter == 0:
                if self.collision_flag:
                    self.update_on_collision()
                else:
                    self.update_on_success()

    '''
    Skip forward a set amount of slots. 
    If used, run on both stations and update access point's counter so everything stays in sync.
    '''
    def skip_counter(self, slots):
        self.counter -= slots

    '''
    Check if the station is transmitting. Used for detecting collisions.
    '''
    def is_xmitting(self):
        xmit_flag = self.status == StationStatus.SENDING or self.vcs_status == VCSStatus.REQUEST_TO_SEND
        ht_sifs_flag = self.status == StationStatus.WAITING_FOR_SIFS and self.is_hidden_terminals and self.vcs_status == VCSStatus.NONE
        return xmit_flag or ht_sifs_flag
    
    '''
    Check conditions when the station should have the channel reserved until the end of its transmission.
    Assumes that checks for collision with another station have already been done.
    Dependent on the topology being used. Not applicable to Hidden Terminals without VCS.
    '''
    def is_reserving_channel(self):
        scd_flag = self.status == StationStatus.SENDING
        scd_vcs_flag = self.status == StationStatus.SENDING_RTS and not self.is_hidden_terminals
        ht_vcs_flag = self.status == self.is_hidden_terminals and self.vcs_status == VCSStatus.CLEAR_TO_SEND
        return scd_flag or scd_vcs_flag or ht_vcs_flag
    
    '''
    On successful transmission, increment successes, reset contention window, and consider the next arrival.
    '''
    def update_on_success(self):
        self.successes += 1
        self.curr_CW = DEFAULT_CW
        self.get_frame_if_available()

    '''
    On collision, increment collisions and double the contention window. Return to sensing and retry.
    '''
    def update_on_collision(self):
        self.collisions += 1
        self.update_CW()
        self.collision_flag = False
        self.switch_to_status(StationStatus.SENSING)

    '''
    Double the size of the station's contention window, as long as the contention window isn't maxed yet
    '''
    def update_CW(self):
        tmp_CW = self.curr_CW * 2
        if tmp_CW > CW_MAX:
            tmp_CW = CW_MAX
        self.curr_CW = tmp_CW

    '''
    Consider the next arrival if there are still frames that need to be transmitted.
    Otherwise, all arrivals have been transmitted and the station is done.
    '''
    def get_frame_if_available(self):
        if (self.frame_index < len(self.frames)-1):
            self.frame_index += 1
            self.switch_to_status(StationStatus.FREE)
        else:
            self.switch_to_status(StationStatus.DONE)
