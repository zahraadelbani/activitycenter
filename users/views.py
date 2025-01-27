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
        role = request.POST['role']  # ClubLeader, Executive, etc.

        # Role-based user creation
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
            return JsonResponse({'error': 'Invalid role selected'}, status=400)
        
        user.save()
        return redirect('list_users')

    return render(request, 'users/create_user.html')

def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.name = request.POST['name']
        user.email = request.POST['email']
        user.status = request.POST['status']
        user.role = request.POST['role']  # Update the role
        user.save()
        return redirect('list_users')

    return render(request, 'users/update_user.html', {'user': user})


# Delete User
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('list_users')
