from typing import Optional

from pydantic import EmailStr
from models.utilities import BaseOrjsonModel


class User(BaseOrjsonModel):
    first_name: Optional[str]
    email: EmailStr
