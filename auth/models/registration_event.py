from pydantic import UUID4, BaseModel


class RegistrationUserEventModel(BaseModel):
    """Модель данных события регистрации пользователя."""

    user_id: UUID4
    firstname: str
    email: str
