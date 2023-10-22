from enum import Enum

class StationStatus(Enum):
    SENSING = 1
    WAITING_FOR_NAV = 2
    BACKOFF = 3
    SENDING = 4
    FREE = 5
    WAITING_FOR_ACK = 6
    ACK = 7
    DONE = 8