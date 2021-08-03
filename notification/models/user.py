from typing import Optional

from pydantic import EmailStr, BaseModel


class User(BaseModel):
    first_name: Optional[str]
    email: EmailStr
