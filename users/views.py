from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import User, ClubLeader, Executive, Rector, ActivityCenterAdmin, ClubMember


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
        return redirect('list_users')

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
        return redirect('list_users')

    return render(request, 'users/update_user.html', {'user': user})

# Delete User
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('list_users')
