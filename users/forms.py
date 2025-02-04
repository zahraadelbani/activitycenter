from allauth.account.forms import SignupForm
from django import forms
from .models import User

class CustomSignupForm(SignupForm):
    """ Custom Signup Form that removes username and only requires email & name """

    name = forms.CharField(max_length=255, required=True, label="Full Name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Explicitly remove 'username' from fields if it exists
        if "username" in self.fields:
            del self.fields["username"]

    def save(self, request):
        """ Ensure the user is saved without a username """
        user = super().save(request)
        user.name = self.cleaned_data["name"]
        user.save()
        return user
