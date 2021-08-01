from typing import Optional

from pydantic import EmailStr
from utilities import BaseOrjsonModel


class User(BaseOrjsonModel):
    first_name: Optional[str]
    email: EmailStr
