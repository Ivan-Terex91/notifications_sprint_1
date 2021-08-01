from dataclasses import dataclass
from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class AdministrationEventModel(TimeStampedModel):
    """Модель события для отправки пользователю уведомления"""
    id = models.UUIDField(_('идентификатор события'), primary_key=True, default=uuid4, editable=False)
    firstname = models.CharField(_('Имя пользователя'), max_length=255)
    subject = models.CharField(_('Тема письма'), max_length=255)
    text = models.TextField(_('Текст письма'))
    email = models.EmailField(_('Почта пользователя'))

    class Meta:
        verbose_name = _('Событие')
        verbose_name_plural = _('События')

    def __str__(self):
        return f"{self.firstname} - {self.subject}"


@dataclass
class UserDataToSend:
    """Данные пользователя для отправки"""
    firstname: str
    subject: str
    text: str
    email: str
