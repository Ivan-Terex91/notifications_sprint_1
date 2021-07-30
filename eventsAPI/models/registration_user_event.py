from pydantic import UUID4, BaseModel, EmailStr


class RegistrationUserEventModel(BaseModel):
    """Модель данных события регистрации пользователя."""

    user_id: UUID4
    firstname: str
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "user_id": "2831e77b-463d-4678-b261-cb52684db28a",
                "firstname": "Bob",
                "email": "Bob@yandex.ru",
            }
        }
