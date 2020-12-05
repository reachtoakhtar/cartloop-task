from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from chat.models import Chat, Conversation
from chat.serializers import ChatCreateSerializer, ConversationSerializer


class ConversationView(RetrieveAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ChatView(CreateAPIView):
    model_class = Chat
    serializer_class = ChatCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        return Response({"chatId": instance.id}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()
