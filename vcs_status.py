from enum import Enum

class VCSStatus(Enum):
    NONE = 1
    REQUEST_TO_SEND = 2
    NO_AP_RESPONSE = 3
    CLEAR_TO_SEND = 4