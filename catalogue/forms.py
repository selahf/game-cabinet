# how does a user enter or edit data?

from django import forms
from django.utils import timezone
from .models import Game

class GameForm(forms.ModelForm):
    class Meta:
        model = Game # which model to use
        fields = [ # fields that users can edit
            "name",
            "description",
            "publisher",
            "image_url",
            "image",
            "year_published",
            "genres",
            "min_players",
            "max_players",
            "play_time_minutes",
            "min_age",
            "complexity"
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.required = field_name == "name" # only required field is name
            
    def clean(self):
        # get cleaned and validated form data
        cleaned_data = super().clean()
        
        # retrieve min and max player counts
        min_players = cleaned_data.get("min_players")
        max_players = cleaned_data.get("max_players")
        
        if ( # check if both are provided
            min_players is not None
            and max_players is not None
            and max_players < min_players
        ):
            self.add_error(
                "max_players",
                "Maximum players cannot be less than minimum players."
            )
        return cleaned_data
    
    def clean_year_published(self):
        year = self.cleaned_data.get("year_published")
        
        if year is not None and year > timezone.localdate().year:
            raise forms.ValidationError(
                "Publication year cannot be in the future."
            )
        return year