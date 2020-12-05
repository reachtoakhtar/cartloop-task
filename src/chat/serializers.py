__author__ = "akhtar"

import re

from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from chat.models import Chat, Conversation

payload_re = re.compile(r"^[a-zA-Z0-9{}$%_\-\\/~@#^&*()!?.]+$")
message = _("Payload must contain characters alphanumeric characters and the following special characters - {}$%_-\/~@#^&*()!?.")
validate_payload = RegexValidator(payload_re, message, status.HTTP_400_BAD_REQUEST)

UserModel = get_user_model()


class ChatCreateSerializer(serializers.ModelSerializer):
    conversationId = serializers.IntegerField()
    chat = serializers.DictField()
    payload = serializers.CharField(required=False)
    user = serializers.IntegerField(required=False)
    conversation = serializers.IntegerField(required=False)
    
    class Meta:
        model = Chat
        fields = "__all__"
    
    def validate(self, attrs):
        conversationId = attrs.get("conversationId")
        chat = attrs.get("chat")
        
        payload = chat["payload"]
        userId = chat["userId"]
        
        payload_to_validate = payload.replace(" ", "")
        validate_payload(payload_to_validate)
        if len(payload) > 300:
            raise ValidationError(_("Length of payload must be less than 300."))
        
        # conversation = Conversation.objects.get(id=conversationId)
        attrs["conversation"] = Conversation.objects.get(pk=conversationId)
        attrs["user"] = UserModel.objects.get(pk=userId)
        attrs["payload"] = payload
        
        attrs.pop("conversationId")
        attrs.pop("chat")
        return attrs

    def create(self, validated_data):
        return super().create(validated_data)
    
    
class ChatSerializer(serializers.ModelSerializer):
    chatId = serializers.IntegerField(source="id")
    userId = serializers.IntegerField(source="user.id")
    
    class Meta:
        model = Chat
        fields = ("chatId", "payload", "userId", "utcdate", "status")


class ConversationSerializer(serializers.ModelSerializer):
    conversationId = serializers.IntegerField(source="id")
    storeId = serializers.IntegerField(source="store.id")
    operatorId = serializers.SerializerMethodField()
    clientId = serializers.SerializerMethodField()
    operatorGroup = serializers.SerializerMethodField()
    chat = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ("conversationId", "storeId", "operatorId", "clientId",
                  "operatorGroup", "chat")
    
    def get_operatorGroup(self, value):
        user_ids = list(set(list(value.chats.values_list("user", flat=True))))
        users = UserModel.objects.filter(id__in=user_ids, is_staff=True)
        if users:
            return users[0].groups.first().name
    
        return None
    
    def get_chat(self, value):
        chats = value.chats.all()
        return ChatSerializer(chats, many=True).data
    
    def get_operatorId(self, value):
        user_ids = list(set(list(value.chats.values_list("user", flat=True))))
        users = UserModel.objects.filter(id__in=user_ids, is_staff=True)
        if users:
            return users[0].id
        
        return None

    def get_clientId(self, value):
        user_ids = list(set(list(value.chats.values_list("user", flat=True))))
        users = UserModel.objects.filter(id__in=user_ids, is_staff=False)
        if users:
            return users[0].id
        
        return None
