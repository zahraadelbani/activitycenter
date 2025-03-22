from users.models import Membership

def membership_roles(request):
    if not request.user.is_authenticated:
        return {}
    
    is_leader = Membership.objects.filter(user=request.user, membership_type="leader").exists()
    is_member = Membership.objects.filter(user=request.user, membership_type="member").exists()
    
    return {
        "is_leader": is_leader,
        "is_member": is_member,
    }
