import pytz
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class Store(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')


class Chat(models.Model):
    chatId = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name="chats")
    payload = models.TextField()
    utcdate = models.DateTimeField()
    
    STATUS_DEFAULT = STATUS_NEW = "new"
    STATUS_SENT = "sent"
    STATUSES = [
        (STATUS_NEW, _("New")),
        (STATUS_SENT, _("Sent")),
    ]
    status = models.CharField(
        max_length=8,
        choices=STATUSES,
        default=STATUS_DEFAULT,
    )


class Conversation(models.Model):
    conversationId = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.PROTECT, null=True)
    clientId = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name="client_convs", null=True)
    operatorId = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name="operator_convs", null=True)


class Schedule(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.PROTECT, related_name="schedule")
    clientId = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name="sch_client")
    operatorId = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name="sch_operator")
