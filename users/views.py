from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from clubs.models import Club
from .models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from users.models import Membership
from django.http import JsonResponse
from django.core.exceptions import ValidationError
@login_required 
def user_dashboard(request):
    user = request.user

    # Check if user is already accepted as a member
    if Membership.objects.filter(user=user, membership_type="member").exists():
        messages.info(request, "You are now a club member!")
        return render(request, "users/udashboard.html")

    # Clubs the user already applied to
    applied_club_ids = Membership.objects.filter(user=user).values_list("club_id", flat=True)

    # Clubs not yet applied to and still have quota
    clubs = Club.objects.exclude(id__in=applied_club_ids)
    clubs = [club for club in clubs if club.get_member_count() < club.quota]

    # Fetch pending applications
    pending_memberships = Membership.objects.filter(user=user, membership_type="pending").select_related("club")

    return render(request, "users/udashboard.html", {
        "clubs": clubs,
        "applied_clubs": applied_club_ids,
        "pending_memberships": pending_memberships
    })

@login_required
def apply_to_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)

    if club.get_member_count() >= club.quota:
        messages.error(request, "This club is full and cannot accept new members.")
        return redirect("users:udashboard")

    if Membership.objects.filter(user=request.user, club=club).exists():
        messages.info(request, "You've already applied to this club.")
    else:
        try:
            Membership.objects.create(user=request.user, club=club, membership_type="pending")
            messages.success(request, f"Application to {club.name} sent!")
        except ValidationError as e:
            messages.error(request, e.messages[0])  

    return redirect("users:udashboard")

@login_required
def check_membership_status(request):
    accepted = Membership.objects.filter(user=request.user, membership_type="member").exists()
    return JsonResponse({"accepted": accepted})

@login_required
def cancel_application(request, club_id):
    membership = get_object_or_404(
        Membership,
        user=request.user,
        club__id=club_id,
        membership_type="pending"
    )
    membership.delete()
    messages.success(request, f"Your application to {membership.club.name} has been withdrawn.")
    return redirect("users:udashboard")

# Navbar
@login_required
def navbar(request):
    return render(request, "navbar.html", {"user": request.user})

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

# List Users
@login_required
def list_users(request):
    role_filter = request.GET.get('role')
    status_filter = request.GET.get('status')

    users = User.objects.all()

    if role_filter:
        users = users.filter(role=role_filter)

    if status_filter:
        users = users.filter(is_active=status_filter)

    roles = User.ROLE_CHOICES
    statuses = User.STATUS_CHOICES

    return render(request, 'users/list_users.html', {
        'users': users,
        'roles': roles,
        'statuses': statuses,
        'selected_role': role_filter,
        'selected_status': status_filter
    })

# Create User (Simple user creation with role assignment)
@login_required
def create_user(request):
    clubs = Club.objects.all()

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        student_id = request.POST['student_id']
        club_id = request.POST.get('club_id')
        membership_type = request.POST.get('membership_type')

        user = User.objects.create_user(email=email, name=name, password=password, role=role, student_id=student_id)

        if club_id:
            club = Club.objects.get(id=club_id)
            Membership.objects.create(user=user, club=club, membership_type=membership_type)

        return redirect('users:list_users')

    return render(request, 'users/create_user.html', {'clubs': clubs})

# Update User (Handle role updates properly)
@login_required
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    memberships = Membership.objects.filter(user=user).select_related("club")

    if request.method == 'POST':
        user.name = request.POST['name']
        user.email = request.POST['email']
        user.student_id = request.POST['student_id']
        user.is_active = request.POST['status']
        user.role = request.POST['role']
        user.save()

        # Track any validation errors
        validation_error_occurred = False

        for membership in memberships:
            field_name = f"membership_type_{membership.id}"
            new_type = request.POST.get(field_name)
            if new_type and new_type != membership.membership_type:
                membership.membership_type = new_type
                try:
                    membership.save()
                except ValidationError as e:
                    messages.error(request, e.messages[0])
                    validation_error_occurred = True

        if validation_error_occurred:
            # Reload the form with messages
            return render(request, 'users/update_user.html', {
                'user': user,
                'memberships': memberships,
            })

        messages.success(request, "User and memberships updated successfully.")
        return redirect('users:list_users')

    return render(request, 'users/update_user.html', {
        'user': user,
        'memberships': memberships,
    })


# Delete User
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted.")
    return redirect('users:list_users')
