# Generated by Django 3.1.7 on 2021-05-05 20:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tutorinator', '0003_auto_20210504_1936'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='QueueEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('day', models.DateField(auto_now=True, null=True)),
                ('inQueue', models.BooleanField(default=True)),
                ('sessionBeginTime', models.TimeField(null=True)),
                ('sessionEndTime', models.TimeField(null=True)),
                ('timeLeft', models.DurationField(null=True)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Tutorinator.course')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_queueentry_set', to=settings.AUTH_USER_MODEL)),
                ('tutor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tutor_queueentry_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule', models.CharField(max_length=3000)),
                ('courses', models.ManyToManyField(to='Tutorinator.Course')),
                ('tutor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(auto_now=True, null=True)),
                ('text', models.TextField(max_length=3000)),
                ('queue_entry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Tutorinator.queueentry')),
                ('reporter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
