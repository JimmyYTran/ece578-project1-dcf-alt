# frame size = 1500 bytes * 8 bits/byte = 12000 bits
# FRAME_SIZE_IN_SLOTS = (12000 bits / 10 bits/microsec) / (10 microsec/slot) = 120 slots
# SLOT_DURATION = 10 microseconds/slot
# bw = 10 Mbps = (10 * 10^6 bps)(1 sec / 10^6 microsec) = 10 bits/microsecond
# simTime = (10 sec)(10^6 microsec / 1 sec) / (10 microsec/slot) = 1000000 slots

FRAME_SIZE_IN_SLOTS = 120
SLOT_DURATION = 10
SIFS = 1
DIFS = 4
ACK = 3
RTS = 3
CTS = 3
BANDWIDTH = 10
DEFAULT_CW = 8
CW_MAX = 512
MAX_SIMULATION_SLOTS = 1000000
LAMBDAS = [100, 200, 300, 500, 800, 1000]
