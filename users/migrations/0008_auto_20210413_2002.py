# Generated by Django 3.1.7 on 2021-04-14 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20210413_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentqueue',
            name='timeLeft',
            field=models.DurationField(null=True),
        ),
    ]
