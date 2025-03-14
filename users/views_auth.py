from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from users.forms import CustomSignupForm

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('login')  
        password = request.POST.get('password')

        print(f"Trying to authenticate: {email}")

        if not email or not password:
            messages.error(request, "Please enter both email and password.")
            return render(request, 'account/login.html')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            print("Login successful!")
            return redirect('/dashboard/')
        else:
            messages.error(request, "Invalid email or password.")
            print("Invalid login attempt.")  

    return render(request, 'account/login.html')

def signup_view(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save(request)
            messages.success(request, "Sign-up successful! Please log in.")
            return redirect("/accounts/login/") 
    else:
        form = CustomSignupForm()
    
    return render(request, "account/signup.html", {"form": form})

def custom_logout_view(request):
    """Logs out the user and redirects to login page."""
    logout(request)
    return redirect('/accounts/login/')  

