# Generated by Django 4.2.4 on 2023-08-15 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bot_app", "0002_alter_userstate_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userstate",
            name="current_state",
            field=models.IntegerField(null=True),
        ),
    ]