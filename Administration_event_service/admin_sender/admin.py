import json
import os
from dataclasses import asdict

import requests
from django.contrib import admin

from .models import AdministrationEventModel, UserDataToSend


@admin.register(AdministrationEventModel)
class AdministrationEventModelAdmin(admin.ModelAdmin):
    actions = ["send_email"]

    def send_email(self, request, queryset):
        for person in queryset:
            user_data = UserDataToSend(
                firstname=person.firstname,
                subject=person.subject,
                text=person.text,
                email=person.email,
            )
            requests.post(
                url="".join(
                    (
                        os.getenv("EVENTS_API_BASE_URL", "http://localhost:10000"),
                        os.getenv(
                            "ADMINISTRATION_EVENT_ROUTE", "/administration_event/"
                        ),
                    )
                ),
                data=json.dumps(asdict(user_data), default=str),
            )

    send_email.short_description = "Отправка персонализированного письма пользователю"
