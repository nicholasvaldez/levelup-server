from django.db import models


class Event(models.Model):
    organizer = models.ForeignKey(
        'Gamer', on_delete=models.CASCADE, related_name='organizers')
    name = models.CharField(max_length=155)
    location = models.CharField(max_length=155)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
