from django.shortcuts import render, get_object_or_404, redirect
from .models import User, ClubLeader, Executive, Rector, ActivityCenterAdmin, ClubMember
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import  ProfileUpdateForm

def base_view(request):
    return render(request, 'users/base.html')

@login_required
def profile_view(request):
    user = request.user  # Get the logged-in user
    form = ProfileUpdateForm(instance=user)  # Pre-fill form with user data

    if request.method == "POST":
        # If updating the profile picture
        if "update_picture" in request.POST and "profile_picture" in request.FILES:
            uploaded_file = request.FILES["profile_picture"]
            print(f"Uploaded file: {uploaded_file.name}")  # Debugging

            if user.profile_picture:
                user.profile_picture.delete(save=False)  # Delete old image

            user.profile_picture = uploaded_file
            user.save()  # Save new profile picture

            print(f"New Profile Picture URL: {user.profile_picture.url}")  # Debugging
            messages.success(request, "Profile picture updated successfully!")
            return redirect(request.path)

        # If updating profile details (Name)
        elif "update_profile" in request.POST:
            form = ProfileUpdateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect(request.path)
            else:
                print("Form is NOT valid:", form.errors)  # Debugging

    return render(request, "users/profile.html", {"user": user, "form": form})

""" users dashboard """
#@login_required
def userdashboard(request):
    return render(request, "users/udashboard.html", {"user": request.user})

@login_required
def dashboard(request):
    return render(request, "dashboard.html", {"user": request.user})

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
