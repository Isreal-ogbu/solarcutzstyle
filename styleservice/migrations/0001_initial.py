# Generated by Django 4.1.5 on 2023-02-15 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='offermodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_picture', models.ImageField(upload_to='offer/')),
                ('offer_discription_top', models.CharField(max_length=20)),
                ('offer_discription_button', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='servicemodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_picture', models.ImageField(upload_to='service/')),
                ('service_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='stylemodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style_picture', models.ImageField(upload_to='style/')),
                ('style_description', models.CharField(max_length=50)),
                ('service_picture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='styleservice.servicemodel')),
            ],
        ),
    ]
