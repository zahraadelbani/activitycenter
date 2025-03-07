from django.contrib import admin
from .models import Club, ClubActivity, Meeting, Announcement

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'quota', 'created_at')
    search_fields = ('name',)

@admin.register(ClubActivity)
class ClubActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'club', 'approval_status', 'datetime')  # ✅ Changed 'date' → 'datetime'
    list_filter = ('approval_status',)  
    search_fields = ('title', 'club__name')  

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('id', 'club', 'date_time', 'agenda')
    search_fields = ('agenda',)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'club', 'title', 'created_at')
    search_fields = ('title',)
