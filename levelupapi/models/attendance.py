from django.db import models


class Attendance(models.Model):
    gamer = models.ForeignKey(
        'Gamer', on_delete=models.CASCADE, related_name='gamers_in_attendance')
    event = models.ForeignKey(
        'Event', on_delete=models.CASCADE, related_name='events')
