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
        return f"{self.name} - {self.user.name}"

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
    
    family_favorite = models.BooleanField(default = False)
    notes = models.TextField(blank = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["collection", "item"],
                name = "unique_collection_items"
            )
        ]

    def __str__(self):
        return f"{self.item.name} in {self.collection.name}"

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
            return f"{self.user.name} - {self.item.name}"

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
        return f"{self.user.name} rated {self.item.name}"