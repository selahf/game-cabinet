from django.db import models
from django.conf import settings
from catalogue.models import Game


class GameSession(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete = models.CASCADE,
        related_name = "sessions"
    )
    date_played = models.DateTimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.game.name} - {self.date_played}"

class SessionParticipant(models.Model):
    session = models.ForeignKey(
        GameSession,
        on_delete = models.CASCADE,
        related_name = "participants"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.SET_NULL,
        null=True,
        blank=True,
        related_name = "game_sessions"
    )
    player_name = models.CharField(max_length=100)
    placement = models.PositiveIntegerField(null=True, blank=True)
    is_winner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.player_name} - {self.session.game.name}"