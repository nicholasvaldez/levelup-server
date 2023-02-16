# Generated by Django 4.1.6 on 2023-02-16 15:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='GameType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=155)),
            ],
        ),
        migrations.CreateModel(
            name='Gamer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155)),
                ('maker', models.CharField(max_length=155)),
                ('number_of_players', models.CharField(max_length=2)),
                ('skill_level', models.CharField(max_length=5)),
                ('game_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_types', to='levelupapi.gametype')),
                ('gamer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gamers', to='levelupapi.gamer')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155)),
                ('location', models.CharField(max_length=155)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('description', models.CharField(max_length=250)),
                ('attendees', models.ManyToManyField(related_name='attendees', through='levelupapi.Attendance', to='levelupapi.gamer')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='levelupapi.game')),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organizers', to='levelupapi.gamer')),
            ],
        ),
        migrations.AddField(
            model_name='attendance',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='levelupapi.event'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='gamer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gamers_in_attendance', to='levelupapi.gamer'),
        ),
    ]
