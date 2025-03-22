from django.shortcuts import render, get_object_or_404, redirect
from .models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm

# Navbar
@login_required
def navbar(request):
    return render(request, "navbar.html", {"user": request.user})

from users.models import Membership  # adjust path if different

@login_required
def profile_view(request):
    user = request.user
    form = ProfileUpdateForm(instance=user)

    # Get user's memberships
    leader_memberships = Membership.objects.filter(user=user, membership_type='leader')
    member_memberships = Membership.objects.filter(user=user, membership_type='member')

    if request.method == "POST":
        if "profile_picture" in request.FILES:
            uploaded_file = request.FILES["profile_picture"]
            if user.profile_picture:
                user.profile_picture.delete(save=False)
            user.profile_picture = uploaded_file
            user.save()
            messages.success(request, "Profile picture updated successfully!")
            return redirect(request.path)

        elif "update_profile" in request.POST:
            form = ProfileUpdateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect(request.path)
            else:
                messages.error(request, "Failed to update profile. Please check the form.")

    context = {
        "user": user,
        "form": form,
        "leader_memberships": leader_memberships,
        "member_memberships": member_memberships,
    }
    return render(request, "users/profile.html", context)


# User Dashboard
@login_required
def userdashboard(request):
    return render(request, "users/udashboard.html", {"user": request.user})

# List Users
def list_users(request):
    users = User.objects.all()
    return render(request, 'users/list_users.html', {'users': users})

# Create User (Simple user creation with role assignment)
def create_user(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        user = User.objects.create_user(email=email, name=name, password=password, role=role)
        user.save()
        return redirect('users:list_users')

    return render(request, 'users/create_user.html')

# Update User (Handle role updates properly)
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        status = request.POST['status']
        new_role = request.POST['role']

        user.name = name
        user.email = email
        user.is_active = status
        user.role = new_role
        user.save()

        messages.success(request, "User updated successfully.")
        return redirect('users:list_users')

    return render(request, 'users/update_user.html', {'user': user})

# Delete User
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted.")
    return redirect('users:list_users')
