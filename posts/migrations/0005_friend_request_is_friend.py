# Generated by Django 4.1 on 2022-09-02 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_rename_from_user_friend_request_request_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend_request',
            name='is_friend',
            field=models.BooleanField(default=False),
        ),
    ]
