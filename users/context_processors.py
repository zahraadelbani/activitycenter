from users.models import Membership
from voting.models import Election, Vote, Candidate
from django.utils import timezone

def membership_roles(request):
    if not request.user.is_authenticated:
        return {}

    is_leader = Membership.objects.filter(user=request.user, membership_type="leader").exists()
    is_member = Membership.objects.filter(user=request.user, membership_type="member").exists()

    voting_elections = []
    if is_member:
        active_elections = Election.objects.filter(
            is_active=True,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        )
        voting_elections = [
            e for e in active_elections
            if not Vote.objects.filter(election=e, voter=request.user).exists()
        ]

    election = Election.get_current_election()
    user_already_nominated = False
    if election and election.is_nomination_open():
        user_already_nominated = Candidate.objects.filter(user=request.user, election=election).exists()

    return {
        "is_leader": is_leader,
        "is_member": is_member,
        "election_class": Election,
        "voting_elections": voting_elections,
        "election": election,
        "user_already_nominated": user_already_nominated,
    }