from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class CatalogueItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    publisher = models.CharField(max_length=150, blank=True)
    image_url = models.URLField(blank=True)
    
    image = models.ImageField(
        upload_to = "catalogue_images/",
        null = True,
        blank = True
    )

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    genre_id = models.BigAutoField(primary_key = True)
    name = models.CharField(max_length = 100, unique = True)
    
    def __str__(self):
        return self.name

class Game(CatalogueItem):
    year_published = models.PositiveSmallIntegerField(
        null = True,
        blank = True
    )
    
    # game classification: games can belong to multiple genres
    genres = models.ManyToManyField(
        Genre,
        blank = True,
        related_name = "games"
    )
    
    # player and gameplay information
    min_players = models.PositiveSmallIntegerField(
        null = True,
        blank = True,
        validators = [MinValueValidator(1)]
    )
    max_players = models.PositiveSmallIntegerField(
        null = True,
        blank = True,
        validators = [MinValueValidator(1)]
    )
    play_time_minutes = models.PositiveIntegerField(
        null = True,
        blank = True,
        validators = [MinValueValidator(1)]
    )
    min_age = models.PositiveSmallIntegerField(
        null = True,
        blank = True
    )
    
    # complexity rating (1.0 to 5.0)
    complexity = models.DecimalField(
        max_digits = 2,
        decimal_places = 1,
        null = True,
        blank = True,
        validators = [
            MinValueValidator(1.0),
            MaxValueValidator(5.0)
        ]
    )

    def __str__(self):
        return self.name

class Puzzle(CatalogueItem):
    piece_count = models.PositiveIntegerField()
    difficulty = models.CharField(max_length=50)

    def __str__(self):
        return self.name