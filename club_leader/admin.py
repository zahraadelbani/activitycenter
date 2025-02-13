from django.contrib import admin
from clubs.models import ClubDocument

# Register ClubDocument model in the admin site
@admin.register(ClubDocument)
class ClubDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'club', 'uploaded_at')  # Removed uploaded_by
    search_fields = ('title', 'club__name')
    list_filter = ('club', 'uploaded_at')