from django.contrib import admin
from django.utils import timezone
from .models import MembershipTerminationRequest

""" 
@admin.register(ClubMember)
class ClubMemberAdmin(admin.ModelAdmin):
    Admin interface for managing club memberships.
    list_display = ('user', 'club', 'joined_at')
    list_filter = ('club', 'joined_at')
    search_fields = ('user__name', 'club__name')
    ordering = ('-joined_at',)
    date_hierarchy = 'joined_at'
 """

@admin.register(MembershipTerminationRequest)
class MembershipTerminationRequestAdmin(admin.ModelAdmin):
    """Admin interface for handling membership termination requests."""
    list_display = ('club_member', 'club', 'status', 'created_at', 'reviewed_at')
    list_filter = ('status', 'club', 'created_at')
    search_fields = ('club_member__user__name', 'club__name')
    ordering = ('-created_at',)
    actions = ['approve_requests', 'reject_requests']
    date_hierarchy = 'created_at'

    def approve_requests(self, request, queryset):
        """Mark selected termination requests as approved."""
        queryset.update(status="approved", reviewed_at=timezone.now())
        self.message_user(request, "Selected requests have been approved.")

    def reject_requests(self, request, queryset):
        """Mark selected termination requests as rejected."""
        queryset.update(status="rejected", reviewed_at=timezone.now())
        self.message_user(request, "Selected requests have been rejected.")

    approve_requests.short_description = "Approve selected termination requests"
    reject_requests.short_description = "Reject selected termination requests"
