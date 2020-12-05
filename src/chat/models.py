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
    
    def __str__(self):
        return self.name


class Conversation(models.Model):
    store = models.ForeignKey(Store, on_delete=models.PROTECT, null=True)
    dicountCode = models.CharField(max_length=8, blank=True, null=True)


class Chat(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name="user_chats")
    payload = models.TextField()
    utcdate = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.PROTECT, related_name="chats")
    
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


class Schedule(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.PROTECT, related_name="schedule")
    client = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name="sch_client")
    operator = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name="sch_operator")
