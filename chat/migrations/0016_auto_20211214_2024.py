# Generated by Django 3.2.8 on 2021-12-14 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0015_alter_information_imagelink'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roomhistory',
            name='status',
        ),
        migrations.AddField(
            model_name='information',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
