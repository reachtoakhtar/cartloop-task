from django.contrib import admin

from .models import CLGroup, CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "is_superuser", "is_staff", "timezone"]
    

class CLGroupAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CLGroup._meta.fields]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CLGroup, CLGroupAdmin)
