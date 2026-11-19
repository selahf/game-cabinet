from django.db import models


class CatalogueItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    publisher = models.CharField(max_length=150, blank=True)
    image_url = models.URLField(blank=True)
    recommended_age = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Game(CatalogueItem):
    min_players = models.PositiveIntegerField()
    max_players = models.PositiveIntegerField()
    estimated_playtime = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Puzzle(CatalogueItem):
    piece_count = models.PositiveIntegerField()
    difficulty = models.CharField(max_length=50)

    def __str__(self):
        return self.name