from pydantic import UUID4, BaseModel, EmailStr


class AdministrationEventModel(BaseModel):
    """Модель данных события от администратора."""

    user_id: UUID4
    firstname: str
    subject: str
    text: str
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "user_id": "2831e77b-463d-4678-b261-cb52684db28a",
                "firstname": "Bob",
                "subject": "Специальное предложение",
                "text": "Добрый день, Bob. Специальное предложение, только для Вас...",
                "email": "Bob@yandex.ru",
            }
        }
