from enum import Enum

from pydantic import BaseModel


class TypeBox(BaseModel):
    id: int | None = None
    name: str

class SponsorLevel(Enum):
    MAIN = "Main"
    PLATINUM = "Platinum"
    GOLD = "Gold"
    SILVER = "Silver"
    BRONZE = "Bronze"
    MEDIA_PARTNER = "Media_partner"


class TypeObject(Enum):
    TALK = "talk"
    SPONSOR = "sponsor"