from pydantic import BaseModel, EmailStr


class AdministrationEventModel(BaseModel):
    """Модель данных события от администратора."""

    firstname: str
    subject: str
    text: str
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "firstname": "Bob",
                "subject": "Специальное предложение",
                "text": "Добрый день, Bob. Специальное предложение, только для Вас...",
                "email": "Bob@yandex.ru",
            }
        }
