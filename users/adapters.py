from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from allauth.core.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    """ Prevent Google from signing up new users, only allow logins """

    def is_open_for_signup(self, request, sociallogin):
        """ Allow login only if the email already exists, prevent new signups """
        email = sociallogin.account.extra_data.get("email", None)
        if email and User.objects.filter(email=email).exists():
            return False  # Skip signup if the user exists
        return True  # Prevent signup if the user is new

    def pre_social_login(self, request, sociallogin):
        """ Redirect users to login if they are not found in the database """
        email = sociallogin.account.extra_data.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            sociallogin.connect(request, user)
        else:
            raise ImmediateHttpResponse(redirect("/accounts/login/"))  # Redirect to login page
