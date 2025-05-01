from django.contrib import admin
from .models import Task
from users.models import CustomUser

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'assigned_by', 'status', 'due_date', 'worked_hours')
    list_filter = ('status', 'assigned_by', 'assigned_to')
    search_fields = ('title', 'description', 'completion_report')
    readonly_fields = ('created_at', 'updated_at', 'assigned_by')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == CustomUser.Role.ADMIN:
            return qs.filter(assigned_by=request.user) | qs.filter(assigned_to__assigned_admin=request.user)
        elif request.user.role == CustomUser.Role.USER:
            return qs.filter(assigned_to=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change:
            obj.assigned_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Task, TaskAdmin)