from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'club', 'date', 'location', 'created_by')
    search_fields = ('title', 'club__name', 'location')
    list_filter = ('date', 'club')

