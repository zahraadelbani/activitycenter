from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll, Choice
from .forms import PollForm, ChoiceForm, ChoiceCountForm
from django.contrib.auth.decorators import login_required

def poll_list(request):
    polls = Poll.objects.filter(club=request.user.clubleader.club)
    return render(request, 'polls/poll_list.html', {'polls': polls})

@login_required
def select_num_choices(request):
    """Step 1: Select how many choices to add."""
    if request.method == "POST":
        form = ChoiceCountForm(request.POST)
        if form.is_valid():
            num_choices = int(form.cleaned_data['num_choices'])
            # Correct the redirect
            return redirect('polls:create_poll', num_choices=num_choices)
    else:
        form = ChoiceCountForm()

    return render(request, 'polls/select_num_choices.html', {'form': form})

@login_required
def create_poll(request, num_choices):
    if request.method == "POST":
        poll_form = PollForm(request.POST)
        choice_forms = [ChoiceForm(request.POST, prefix=str(i)) for i in range(num_choices)]
        if poll_form.is_valid() and all(cf.is_valid() for cf in choice_forms):
            poll = poll_form.save(commit=False)
            poll.club = request.user.clubleader.club
            poll.created_by = request.user
            poll.save()
            for choice_form in choice_forms:
                choice = choice_form.save(commit=False)
                choice.poll = poll
                choice.save()
            return redirect('polls:poll_list')
    else:
        poll_form = PollForm()
        choice_forms = [ChoiceForm(prefix=str(i)) for i in range(num_choices)]
    return render(request, 'polls/create_poll.html', {'poll_form': poll_form, 'choice_forms': choice_forms, 'num_choices': num_choices})

@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, club=request.user.clubleader.club)
    if request.method == "POST":
        choice_id = request.POST.get("choice")
        choice = get_object_or_404(Choice, id=choice_id)
        choice.votes += 1
        choice.save()
        return redirect('polls:poll_results', poll_id=poll.id)
    return render(request, 'polls/vote.html', {'poll': poll})

@login_required
def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, club=request.user.clubleader.club)
    return render(request, 'polls/poll_results.html', {'poll': poll})

@login_required
def update_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, club=request.user.clubleader.club)
    choices = poll.choices.all()
    if request.method == "POST":
        poll_form = PollForm(request.POST, instance=poll)
        choice_forms = [ChoiceForm(request.POST, prefix=str(choice.id), instance=choice) for choice in choices]
        new_choice_form = ChoiceForm(request.POST, prefix="new")
        if poll_form.is_valid() and all(cf.is_valid() for cf in choice_forms) and new_choice_form.is_valid():
            poll_form.save()
            for choice_form in choice_forms:
                choice_form.save()
            new_choice = new_choice_form.save(commit=False)
            if new_choice.text.strip():
                new_choice.poll = poll
                new_choice.save()
            return redirect('polls:poll_list')
    else:
        poll_form = PollForm(instance=poll)
        choice_forms = [ChoiceForm(prefix=str(choice.id), instance=choice) for choice in choices]
        new_choice_form = ChoiceForm(prefix="new")
    return render(request, 'polls/update_poll.html', {'poll_form': poll_form, 'choice_forms': choice_forms, 'new_choice_form': new_choice_form, 'poll': poll})


def view_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    return render(request, 'polls/view_poll.html', {'poll': poll})
