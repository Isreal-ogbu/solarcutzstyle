# Generated by Django 4.1.5 on 2023-02-13 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phoneverificationapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonenumbermodel',
            name='verifiednumber',
            field=models.BooleanField(default=False),
        ),
    ]
