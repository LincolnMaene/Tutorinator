# Generated by Django 3.1.7 on 2021-04-13 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210413_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentqueue',
            name='sessionBeginTime',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='studentqueue',
            name='sessionEndTime',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='studentqueue',
            name='timeLeft',
            field=models.TimeField(null=True),
        ),
    ]