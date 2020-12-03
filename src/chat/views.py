from rest_framework.generics import CreateAPIView, RetrieveAPIView

from chat.models import Conversation


class ConversationView(RetrieveAPIView):
    model_class = Conversation
    serializer_class = None
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ChatView(CreateAPIView):
    model_class = Conversation
    serializer_class = None
