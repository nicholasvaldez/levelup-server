from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=155)
    game_type = models.ForeignKey(
        'GameType', on_delete=models.CASCADE, related_name='game_types')
    gamer = models.ForeignKey(
        'Gamer', on_delete=models.CASCADE, related_name='gamers')
    maker = models.CharField(max_length=155)
    number_of_players = models.CharField(max_length=2)
    skill_level = models.CharField(max_length=5)
