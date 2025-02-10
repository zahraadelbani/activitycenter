from django.contrib import admin
from .models import Poll, Choice

class ChoiceInline(admin.TabularInline):  # Allows adding choices inside the poll admin page
    model = Choice
    extra = 2  # Number of empty choices to display

class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at', 'is_active')  # Customize admin list display
    search_fields = ('question',)  # Enable search functionality
    list_filter = ('created_at', 'is_active')  # Enable filtering
    inlines = [ChoiceInline]  # Display choices inside Poll admin page

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)  # Register Choice separately
