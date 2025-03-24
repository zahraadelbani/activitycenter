from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from users.forms import CustomSignupForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from users.models import Membership

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('login')  
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")

            print(f"User {user.email} logged in with role: {user.get_role()}")

            role_redirects = {
                "club_leader": "club_leader:dashboard",
                "club_member": "club_member:dashboard",
                "activity_center_admin": "activity_center_admin:dashboard",
            }
            
            redirect_url = role_redirects.get(user.get_role(), "navbar")  # Default fallback
            return redirect(redirect_url)

        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'account/login.html')


def signup_view(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save(request)
            messages.success(request, "Sign-up successful! Please log in.")
            return redirect("account_login") 
    else:
        form = CustomSignupForm()
    
    return render(request, "account/signup.html", {"form": form})


def custom_logout_view(request):
    """Logs out the user and redirects to login page."""
    logout(request)
    return redirect('account_login')  

@login_required
def redirect_after_login(request):
    user = request.user

    if user.is_superuser:
        return redirect("users:list_users")  # 🔒 Superuser only

    if user.get_role() == "activity_center_admin":
        return redirect("activity_center_admin:dashboard")

    elif Membership.objects.filter(user=user, membership_type="leader").exists():
        return redirect("club_leader:dashboard")

    elif Membership.objects.filter(user=user, membership_type="member").exists():
        return redirect("club_member:dashboard")

    elif user.get_role() == "user":
        return redirect("users:udashboard")

    messages.error(request, "You are not assigned to any club.")
    return redirect("users:profile")




