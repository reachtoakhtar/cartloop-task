__author__ = "akhtar"

from django.contrib.auth import get_user_model

from django.core.management.base import BaseCommand

from custom_user.models import CLGroup

UserModel = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        client1 = "client111222@gmail.com"
        UserModel.objects.create_user(
            email=client1,
            username=client1,
            password=client1,
            timezone="Europe/Berlin",
        )

        client2 = "client111223@gmail.com"
        UserModel.objects.create_user(
            email=client2,
            username=client2,
            password=client2,
            timezone="",
        )
        
        operator1 = "operator111222@gmail.com"
        user = UserModel.objects.create_staff(
            email=operator1,
            username=operator1,
            password=operator1,
            timezone="Europe/Berlin",
        )
        group = CLGroup.objects.filter(pk=1)
        user.groups.set(group)
        user.save()
        
        operator2 = "operator111223@gmail.com"
        user = UserModel.objects.create_staff(
            email=operator2,
            username=operator2,
            password=operator2,
            timezone="",
        )
        group = CLGroup.objects.filter(pk=2)
        user.groups.set(group)
        user.save()
        
        self.stdout.write(
            self.style.SUCCESS("Successfully added clients and operators."))
