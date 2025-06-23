from datetime import datetime

from pydantic import BaseModel

from app.auth.roles import Role


class User(BaseModel):
    uid: str | None = None
    name: str
    email: str
    role: Role
    password: str
    phone_number: str| None = None
    photo_url: str| None = None
    email_verified: bool | None = False
    disabled: bool | None = False
    creation_date: datetime = datetime.now()
    last_modification_date: datetime = datetime.now()
    user_last_modified: str | None = None