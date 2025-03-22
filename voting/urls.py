from django.urls import path
from .views import active_elections, candidate_list, cast_vote, verify_results, thank_you, election_results, already_voted, self_nominate

app_name = "voting"

urlpatterns = [
    path("elections/", active_elections, name="elections"),
    path("elections/<int:election_id>/position/<int:position_id>/", candidate_list, name="candidates"),
    path("vote/<int:election_id>/<int:position_id>/<int:candidate_id>/", cast_vote, name="vote"),
    path("results/<int:election_id>/", election_results, name="results"),
    path("verify/<int:election_id>/", verify_results, name="verify_results"),
    path('thank-you/', thank_you, name='thank_you'),
    path('already-voted/', already_voted, name='already_voted'),
    path("self-nominate/", self_nominate, name="self_nominate"),
]
