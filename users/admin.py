from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'assigned_admin')
    list_filter = ('role',)
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role', 'assigned_admin')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role', 'assigned_admin')}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == CustomUser.Role.ADMIN:
            return qs.filter(assigned_admin=request.user)
        return qs

    def has_change_permission(self, request, obj=None):
        if obj and request.user.role == CustomUser.Role.ADMIN:
            return obj.assigned_admin == request.user
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and request.user.role == CustomUser.Role.ADMIN:
            return False  # Admins can't delete users
        return super().has_delete_permission(request, obj)

admin.site.register(CustomUser, CustomUserAdmin)