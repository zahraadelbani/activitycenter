from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone

from .forms import SelfNominationForm
from .models import Election, Candidate, Vote, Position
from users.models import Membership

@login_required
def active_elections(request):
    elections = Election.objects.filter(is_active=True, start_date__lte=timezone.now(), end_date__gte=timezone.now())
    elections = [e for e in elections if not Vote.objects.filter(election=e, voter=request.user).exists()]
    return render(request, "voting/elections.html", {"elections": elections})

@login_required
def cast_vote(request, election_id, position_id, candidate_id):
    election = get_object_or_404(Election, id=election_id, is_active=True)
    position = get_object_or_404(Position, id=position_id)
    candidate = get_object_or_404(Candidate, id=candidate_id, position=position, election=election)

    if request.user.role != "club_member":
        messages.error(request, "Only club members are allowed to vote.")
        return redirect("voting:already_voted")

    if timezone.now() > election.end_date:
        messages.error(request, "Voting is closed for this election.")
        return redirect("voting:already_voted")

    if Vote.objects.filter(election=election, voter=request.user, position=position).exists():
        messages.warning(request, "You have already voted for this position.")
        return redirect("voting:already_voted")

    Vote.objects.create(election=election, voter=request.user, position=position, candidate=candidate)
    candidate.votes += 1
    candidate.save()

    messages.success(request, "Your vote has been submitted successfully.")
    return redirect("voting:thank_you")

@staff_member_required
def verify_results(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    election.results_verified = True
    election.save()
    return redirect("voting:results", election_id=election.id)

@login_required
def candidate_list(request, election_id, position_id):
    election = get_object_or_404(Election, id=election_id, is_active=True)
    position = get_object_or_404(Position, id=position_id, election=election)
    candidates = Candidate.objects.filter(election=election, position=position, approved=True)
    return render(request, "voting/candidates.html", {"election": election, "position": position, "candidates": candidates})

@login_required
def already_voted(request):
    return render(request, 'voting/already_voted.html')

@login_required
def thank_you(request):
    return render(request, 'voting/thank_you.html')

@login_required
def election_results(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    candidates = Candidate.objects.filter(election=election).order_by('-votes')
    return render(request, "voting/results.html", {"election": election, "candidates": candidates})

@login_required
def self_nominate(request):
    if not Membership.objects.filter(user=request.user, membership_type="member").exists():
        messages.error(request, "Only club members can nominate themselves for elections.")
        return redirect("users:udashboard")

    if request.method == "POST":
        form = SelfNominationForm(request.POST, user=request.user)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, "Your nomination has been submitted for admin approval.")
            return redirect("users:udashboard")
    else:
        form = SelfNominationForm(user=request.user)

    return render(request, "voting/self_nomination.html", {"form": form})