from django.db import models


class Collection(models.Model):
    collection_name = models.CharField(max_length=200)

    def __str__(self):
        return self.collection_name
