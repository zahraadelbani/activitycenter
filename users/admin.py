from django.contrib import admin
from .models import User, ClubLeader, Executive, Rector, ActivityCenterAdmin, ClubMember

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'status', 'is_admin')
    search_fields = ('name', 'email')
    list_filter = ('status', 'is_admin')

admin.site.register(ClubLeader)
admin.site.register(Executive)
admin.site.register(Rector)
admin.site.register(ActivityCenterAdmin)

@admin.register(ClubMember)
class ClubMemberAdmin(admin.ModelAdmin):
    """Admin interface for managing club memberships."""
    list_display = ('user', 'club', 'joined_at')
    list_filter = ('club', 'joined_at')
    search_fields = ('user__name', 'club__name')
    ordering = ('-joined_at',)
    date_hierarchy = 'joined_at'