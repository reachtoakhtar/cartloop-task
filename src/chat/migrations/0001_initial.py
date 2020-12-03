# Generated by Django 3.1.3 on 2020-12-03 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('chatId', models.AutoField(primary_key=True, serialize=False)),
                ('payload', models.TextField()),
                ('utcdate', models.DateTimeField()),
                ('status', models.CharField(choices=[('new', 'New'), ('sent', 'Sent')], default='new', max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('conversationId', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='schedule', to='chat.chat')),
            ],
        ),
    ]