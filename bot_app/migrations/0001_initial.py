# Generated by Django 4.2.4 on 2023-08-15 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.IntegerField(unique=True)),
                ("username", models.TextField(null=True, unique=True)),
                ("first_name", models.TextField(null=True)),
                ("last_name", models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="UserState",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("command", models.CharField(max_length=50)),
                ("current_state", models.IntegerField()),
                ("data_state", models.TextField(null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bot_app.user",
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Savings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("savings_type", models.TextField()),
                ("quantity", models.IntegerField(null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="bot_app.user"
                    ),
                ),
            ],
        ),
    ]