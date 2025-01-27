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
admin.site.register(ClubMember)
