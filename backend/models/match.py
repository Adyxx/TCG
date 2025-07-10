from django.db import models
from .users import User

class Match(models.Model):
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_player1')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_player2')
    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='wins')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Match {self.id} between {self.player1} and {self.player2}"
