from enum import Enum

class VCSStatus(Enum):
    NONE = 1
    REQUEST_TO_SEND = 2
    CLEAR_TO_SEND = 3