# Generated by Django 5.1.3 on 2024-11-05 21:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="flaggedmessage",
            name="client_msg_id",
            field=models.CharField(default=None, max_length=255, unique=True),
        ),
    ]
