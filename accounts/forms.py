
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.db import transaction
from collection.models import Collection

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):

    # adds a field for a user's first collection during registration
    collection_name = forms.CharField(
        max_length=100,
        label="Name your first collection",
        help_text="You can create additional collections later!"
    )

    class Meta:
        model = User
        fields = ("identifier", "name")

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            with transaction.atomic():
                user.save()

                Collection.objects.create(
                    user=user,
                    name=self.cleaned_data["collection_name"]
                )

        return user
