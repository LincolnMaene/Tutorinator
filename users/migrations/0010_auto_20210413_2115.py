# Generated by Django 3.1.7 on 2021-04-14 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_sessions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessions',
            name='sessionBeginTime',
            field=models.TimeField(auto_now=True, null=True),
        ),
    ]
