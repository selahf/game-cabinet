from django import forms
from .models import CollectionItem, Collection

class CollectionItemForm(forms.ModelForm):
    class Meta:
        model = CollectionItem
        fields = [
            "collection",
            "family_favorite",
            "notes"
        ]
        
    def __init__(self, *args, user = None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if user is not None:
            self.fields["collection"].queryset = Collection.objects.filter(
                user = user
            )
        else:
            self.fields["collection"].queryset = Collection.objects.none()