from django import forms
from .models import CollectionItem

class CollectionItemForm(forms.ModelForm):
    class Meta:
        model = CollectionItem
        fields = [
            "family_favorite",
            "notes"
        ]