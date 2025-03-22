from django.contrib import admin
from .models import User,Membership

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "role", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("name", "email")

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "club", "membership_type", "created_at")
    list_filter = ("membership_type", "club")
    search_fields = ("user__name", "club__name")