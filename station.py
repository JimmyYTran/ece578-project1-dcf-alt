import numpy as np
from station_status import StationStatus
from parameters import *

class Station:

    def __init__(self, name, lam, sim_time):
        self.success = 0
        self.collisions = 0
        self.curr_CW = DEFAULT_CW
        self.name = name
        self.buffer = []
        self.slots_with_frame = []
        self.status = StationStatus.FREE
        self.lam = lam
        
        running_sum = 0
        avg_slot_arrival = (1/self.lam)/SLOT_DURATION
        while running_sum < MAX_SIMULATION_SLOTS:
            running_sum += np.random.poisson(lam=avg_slot_arrival)
            self.slots_with_frame.append(running_sum)