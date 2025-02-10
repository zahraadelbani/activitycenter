from django.contrib import admin
from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("submitted_by", "club", "category", "status", "created_at")
    list_filter = ("category", "status", "created_at")
    search_fields = ("submitted_by__name", "club__name", "content")

admin.site.register(Feedback, FeedbackAdmin)
