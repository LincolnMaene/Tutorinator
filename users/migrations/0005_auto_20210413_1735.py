# Generated by Django 3.1.7 on 2021-04-13 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_studentqueue_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentqueue',
            name='student_id',
            field=models.IntegerField(),
        ),
    ]