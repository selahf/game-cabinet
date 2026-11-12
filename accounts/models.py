from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=100)
    studio = models.CharField(max_length=100)
    # can add more attributes here.

    def __str__(self):
        return self.title
