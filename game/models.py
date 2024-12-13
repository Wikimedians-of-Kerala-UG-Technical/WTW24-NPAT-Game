from django.db import models
import random
import string

def get_random_letter():
    return random.choice(string.ascii_uppercase)

class Game(models.Model):
    room_code = models.CharField(max_length=8, unique=True)
    creator_name = models.CharField(max_length=100)
    rounds = models.IntegerField(choices=[(5, '5'), (7, '7'), (10, '10')])
    scoring_method = models.CharField(max_length=20, choices=[('Score Each Other', 'Score Each Other'), ('Score Yourself', 'Score Yourself')])
    created_at = models.DateTimeField(auto_now_add=True)
    letter = models.CharField(max_length=1, default=get_random_letter)  # Use method reference


class Player(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='players')
    name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
