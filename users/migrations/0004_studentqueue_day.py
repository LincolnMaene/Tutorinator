# Generated by Django 3.1.7 on 2021-04-12 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_studentqueue'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentqueue',
            name='day',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
