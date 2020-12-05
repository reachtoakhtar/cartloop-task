from django.db.models.signals import post_save
from django.dispatch import receiver

from chat.models import Chat, Conversation, Schedule


@receiver(post_save, sender=Chat)
def postsave_chat(instance, **kwargs):
    conversation = Conversation.objects.get(pk=instance.conversation.pk)
    
    if instance.user.is_staff:
        conversation.operator = instance.user
    if not instance.user.is_staff:
        conversation.client = instance.user

    conversation.save()
    
    Schedule.objects.create(
        chat=instance,
        client=conversation.client,
        operator=conversation.operator)
    
    return instance
