from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Login View
def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        print(f"Trying to authenticate: {email}")  # Debugging line

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            print("Login successful!")  # Debugging line
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password.")
            print("Invalid login attempt.")  # Debugging line

    return render(request, 'users/login.html')
