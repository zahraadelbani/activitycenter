from django.urls import path
from . import views

app_name = "clubs"

urlpatterns = [
    path("<int:club_id>/", views.club_detail, name="club_detail"),
]
