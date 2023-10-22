from enum import Enum

class StationStatus(Enum):
    SENSING = 1
    WAITING_FOR_NAV = 2
    BACKOFF = 3
    SENDING = 4
    FREE = 5
    WAITING_FOR_SIFS = 6
    WAITING_FOR_ACK = 7
    SENDING_RTS = 8
    WAITING_FOR_CTS = 9
    DONE = 10