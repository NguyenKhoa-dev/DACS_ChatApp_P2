# Generated by Django 3.2.9 on 2021-11-29 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20211129_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='room',
            field=models.CharField(max_length=255),
        ),
        migrations.DeleteModel(
            name='Room',
        ),
    ]
