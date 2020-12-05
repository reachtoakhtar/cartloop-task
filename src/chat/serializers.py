__author__ = "akhtar"

import re

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from chat.models import Chat, Conversation

payload_re = re.compile(r"^[a-zA-Z0-9{}$%_\-\\/~@#^&*()!?.]+$")
message = _("Payload must contain alphanumeric characters and only these special characters {}$%_-\/~@#^&*()!?.")
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
        
        attrs["conversation"] = Conversation.objects.get(pk=conversationId)
        attrs["user"] = UserModel.objects.get(pk=userId)
        attrs["payload"] = payload
        
        attrs.pop("conversationId")
        attrs.pop("chat")
        return attrs
    
    
class ChatSerializer(serializers.ModelSerializer):
    chatId = serializers.IntegerField(source="id")
    payload = serializers.SerializerMethodField()
    userId = serializers.IntegerField(source="user.id")
    
    class Meta:
        model = Chat
        fields = ("chatId", "payload", "userId", "utcdate", "status")

    def get_payload(self, value):
        payload = value.payload
        if value.conversation.client is not None:
            payload = payload.replace("{{username}}", value.conversation.client.username)
            payload = payload.replace("{{ username }}", value.conversation.client.username)
        if value.conversation.operator is not None:
            payload = payload.replace("{{operator.Name}}", value.conversation.operator.first_name)
            payload = payload.replace("{{ operator.Name }}", value.conversation.operator.first_name)
        if value.conversation.dicountCode:
            payload = payload.replace("{{discountCode}}", value.conversation.dicountCode)
            payload = payload.replace("{{ discountCode }}", value.conversation.dicountCode)
        
        return payload
    
    
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
        if value.operator is not None:
            groups = value.operator.groups.all()
            if groups:
                return groups[0].name

    def get_chat(self, value):
        chats = value.chats.all()
        return ChatSerializer(chats, many=True).data
    
    def get_operatorId(self, value):
        if value.operator is not None:
            return value.operator.id

    def get_clientId(self, value):
        if value.client is not None:
            return value.client.id
