# Generated by Django 3.1.7 on 2021-04-23 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_timeoffrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoffrequest',
            name='schedule',
            field=models.CharField(max_length=3000),
        ),
    ]
