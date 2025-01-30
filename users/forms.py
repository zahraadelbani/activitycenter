from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    """ Custom Signup Form to replace username with name """

    name = forms.CharField(max_length=255, required=True, label="Full Name")

    def save(self, request):
        """ Save method to ensure name is stored """
        user = super().save(request)
        user.name = self.cleaned_data["name"]
        user.save()
        return user