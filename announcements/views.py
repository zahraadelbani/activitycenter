from django.shortcuts import render

# Create your views here.

def list_announcements(request):
    
    return render(request, "announcements/list_announcements.html")