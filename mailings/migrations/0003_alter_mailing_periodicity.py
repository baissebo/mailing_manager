# Generated by Django 4.2.2 on 2024-07-18 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailings", "0002_alter_mailing_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="periodicity",
            field=models.CharField(
                choices=[
                    ("daily", "Раз в день"),
                    ("weekly", "Раз в неделю"),
                    ("monthly", "Раз в месяц"),
                ],
                max_length=50,
                verbose_name="Периодичность",
            ),
        ),
    ]
