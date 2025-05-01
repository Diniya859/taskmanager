from rest_framework.permissions import BasePermission
from users.permissions import IsAdmin, IsSuperAdmin

class IsTaskOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.assigned_to == request.user

class CanManageTasks(IsAdmin):
    pass

class CanViewCompletionReports(IsAdmin):
    pass