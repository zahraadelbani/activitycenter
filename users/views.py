from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import User, ClubLeader, Executive, Rector, ActivityCenterAdmin, ClubMember
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomSignupForm

from django.shortcuts import redirect
from allauth.account.views import SignupView

class CustomSignupView(SignupView):
    success_url = '/accounts/login/'
    
def base_view(request):
    return render(request, 'users/base.html')

@login_required
def profile_view(request):
    user = request.user  # Get the logged-in user

    if request.method == "POST" and "profile_picture" in request.FILES:
        uploaded_file = request.FILES["profile_picture"]
        print(f"Uploaded file: {uploaded_file.name}")  # Debugging

        if user.profile_picture:  
            user.profile_picture.delete(save=False)  # ✅ Delete old image to avoid clutter

        user.profile_picture = uploaded_file
        user.save()  # ✅ Save the new profile picture

        print(f"New Profile Picture URL: {user.profile_picture.url}")  
        return redirect(request.path)  

    return render(request, "users/profile.html", {"user": user})


@login_required
def dashboard(request):
    return render(request, "dashboard.html", {"user": request.user})


def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)  # Authenticate user

        if user is not None:
            login(request, user)  # Log the user in
            messages.success(request, "Login successful!")
            return redirect('dashboard')  # Redirect to a protected page after login
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'users/login.html')  # Make sure this path is correct!

def signup_view(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save(request)  # Save the user but don't log them in
            messages.success(request, "Sign-up successful! Please log in.")
            return redirect("account_login")  # Redirect to the login page instead of dashboard
    else:
        form = CustomSignupForm()
    
    return render(request, "users/signup.html", {"form": form})



# List Users
def list_users(request):
    users = User.objects.all()
    return render(request, 'users/list_users.html', {'users': users})

# Create User
def create_user(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']  # Get the selected role from the form

        # Create user based on the selected role
        if role == 'ClubLeader':
            user = ClubLeader.objects.create_user(email=email, name=name, password=password)
        elif role == 'Executive':
            user = Executive.objects.create_user(email=email, name=name, password=password)
        elif role == 'Rector':
            user = Rector.objects.create_user(email=email, name=name, password=password)
        elif role == 'ActivityCenterAdmin':
            user = ActivityCenterAdmin.objects.create_user(email=email, name=name, password=password)
        elif role == 'ClubMember':
            user = ClubMember.objects.create_user(email=email, name=name, password=password)
        else:
            user = User.objects.create_user(email=email, name=name, password=password)  # Default to User

        user.save()
        return redirect('users:list_users')

    return render(request, 'users/create_user.html')


def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        status = request.POST['status']
        new_role = request.POST['role']

        # Check if the role is actually changing
        if new_role != user.get_role():
            # Get user data before deletion
            password = user.password
            student_id = getattr(user, 'student_id', None)  # Keep student_id if available

            # Delete the old instance
            user.delete()

            # Create a new instance with the selected role
            if new_role == 'ClubLeader':
                user = ClubLeader.objects.create_user(email=email, name=name, password=password)
            elif new_role == 'Executive':
                user = Executive.objects.create_user(email=email, name=name, password=password)
            elif new_role == 'Rector':
                user = Rector.objects.create_user(email=email, name=name, password=password)
            elif new_role == 'ActivityCenterAdmin':
                user = ActivityCenterAdmin.objects.create_user(email=email, name=name, password=password)
            elif new_role == 'ClubMember':
                user = ClubMember.objects.create_user(email=email, name=name, password=password)
            else:
                user = User.objects.create_user(email=email, name=name, password=password)

            # Assign the student ID if applicable
            if student_id:
                user.student_id = student_id

        else:
            # If the role didn't change, just update user details
            user.name = name
            user.email = email
            user.status = status

        user.save()
        return redirect('users:list_users')

    return render(request, 'users/update_user.html', {'user': user})

# Delete User
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('users:list_users')
