# Generated by Django 3.1.3 on 2020-12-03 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chat', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='clientId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sch_client', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='schedule',
            name='operatorId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sch_operator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='conversation',
            name='clientId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='client_convs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='conversation',
            name='operatorId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='operator_convs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='conversation',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='chat.store'),
        ),
        migrations.AddField(
            model_name='chat',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='chats', to=settings.AUTH_USER_MODEL),
        ),
    ]