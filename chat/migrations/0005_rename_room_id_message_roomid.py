# Generated by Django 4.2.2 on 2023-07-12 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_message_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='room_id',
            new_name='roomid',
        ),
    ]
