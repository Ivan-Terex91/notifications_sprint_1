from typing import Optional

from pydantic import EmailStr

from .utils import BaseOrjsonModel


class User(BaseOrjsonModel):
    first_name: Optional[str]
    email: EmailStr
