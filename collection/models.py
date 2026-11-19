from django.db import models
from django.conf import settings
from catalogue.models import CatalogueItem


class Collection(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "collections"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class CollectionItem(models.Model):
    collection = models.ForeignKey(
        Collection,
        on_delete = models.CASCADE,
        related_name = "items"
    )
    item = models.ForeignKey(
        CatalogueItem,
        on_delete = models.CASCADE,
        related_name = "collections"
    )
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["collection", "item"],
                name = "unique_collection_items"
            )
        ]

    def __str__(self):
        return f"{self.item.name} in {self.collection.name}"
    
class Genre(models.Model):
    genre_id = models.BigAutoField(primary_key = True)
    name = models.CharField(max_length = 100, unique = True)
    
    def __str__(self):
        return self.name
    
class Game(models.Model):
    game_id = models.BigAutoField(primary_key = True)
    
    # basic game info
    name = models.CharField(max_length = 200)
    publisher = models.CharField(max_length = 200, blank = True)
    year_published = models.PositiveSmallIntegerField(
        null = True,
        blank = True
    )
    
    # game classification
    genre = models.ForeignKey(
        Genre,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name = "games"
    )
    
    # player and gameplay information
    min_players = models.PositiveSmallIntegerField(
        null = True,
        blank = True
    )
    max_players = models.PositiveSmallIntegerField(
        null = True,
        blank = True
    )
    play_time_minutes = models.PositiveIntegerField(
        null = True,
        blank = True
    )
    min_age = models.PositiveSmallIntegerField(
        null = True,
        blank = True
    )
    
    # complexity rating (1.0 to 5.0)
    # TODO: add validation to enforce rating
    complexity = models.DecimalField(
        max_digits = 2,
        decimal_places = 1,
        null = True,
        blank = True
    )
    
    # personal collection information
    family_favorite = models.BooleanField(default = False)
    image = models.ImageField(
        upload_to = "game_images/",
        null = True,
        blank = True
    )
    notes = models.TextField(blank = True)
    
    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "favorites"
    )
    item = models.ForeignKey(
        CatalogueItem,
        on_delete = models.CASCADE,
        related_name = "favorited_by"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["user", "item"],
                name = "unique_user_favorite"
            )
        ]

        def __str__(self):
            return f"{self.user.username} - {self.item.name}"

class Rating(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "ratings"
    )
    item = models.ForeignKey(
        CatalogueItem,
        on_delete = models.CASCADE,
        related_name = "ratings"
    )
    score = models.PositiveIntegerField()
    review = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["user", "item"],
                name = "unique_user_rating"
            )
        ]

    def __str__(self):
        return f"{self.user.username} rated {self.item.name}"