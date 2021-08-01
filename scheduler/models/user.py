from typing import Optional

from models.utilities import BaseOrjsonModel
from pydantic import EmailStr


class User(BaseOrjsonModel):
    first_name: Optional[str]
    email: EmailStr
