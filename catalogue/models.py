from django.db import models


class Catalogue(models.Model):
    catalogue_name = models.CharField(max_length=200)

    def __str__(self):
        return self.catalogue_name
