from allauth.account.adapter import DefaultAccountAdapter  # ✅ Corrected import
from django.contrib.auth import get_backends, login

class CustomAccountAdapter(DefaultAccountAdapter):  # ✅ Inherit from DefaultAccountAdapter
    def login(self, request, user):
        remember = request.POST.get('remember', None)  # Check if "Remember Me" is checked
        
        # Get the authentication backend
        backend = get_backends()[0].__class__.__name__  # Get the first authentication backend
        user.backend = f'django.contrib.auth.backends.{backend}'

        if remember:
            request.session.set_expiry(1209600)  # 2 weeks
        else:
            request.session.set_expiry(86400)  # Session expires on browser close
        
        login(request, user, backend=user.backend)  # Provide backend explicitly
