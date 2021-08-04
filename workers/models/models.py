from pydantic import BaseModel, EmailStr


class RegistrationEmailModel(BaseModel):
    """Модель события о регистрации пользователя"""

    firstname: str
    email: EmailStr
    subject: str = "registration"


class AdministrationEmail(BaseModel):
    """Модель события от администраторов"""

    firstname: str
    email: EmailStr
    subject: str
    text: str


class SchedulerBookmarksEmail(BaseModel):
    """Модель события закладок фильмов"""

    firstname: str
    email: EmailStr
    subject: str = "Bookmarks"
    films: str


class EmailData(BaseModel):
    """Модель сообщения для отправки по email"""

    email: EmailStr
    subject: str
    text: str
