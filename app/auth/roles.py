from enum import Enum

class Role(Enum):
    ADMIN = "admin"
    ORGANIZER = "organizer"
    SPEAKER = "speaker"
    ATTENDEE = "attendee"