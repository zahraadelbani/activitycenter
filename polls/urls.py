from django.urls import path
from . import views

urlpatterns = [
    path('', views.poll_list, name='poll_list'),
    path('select_num_choices/', views.select_num_choices, name='select_num_choices'),
    path('create/<int:num_choices>/', views.create_poll, name='create_poll'),
    path('<int:poll_id>/vote/', views.vote, name='vote'),
    path('<int:poll_id>/results/', views.poll_results, name='poll_results'),
    path('<int:poll_id>/update/', views.update_poll, name='update_poll'),  # ✅ New update URL
]
