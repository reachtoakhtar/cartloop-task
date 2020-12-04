from django.contrib import admin

from .models import Store, Chat, Conversation, Schedule


class StoreAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Store._meta.fields]


class ChatAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Chat._meta.fields]


class ConversationAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Conversation._meta.fields]


class ScheduleAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Schedule._meta.fields]


admin.site.register(Store, StoreAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Schedule, ScheduleAdmin)
