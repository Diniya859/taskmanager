from django.contrib import admin
from .models import Task, CompletionReport

class CompletionReportInline(admin.StackedInline):
    model = CompletionReport
    extra = 0

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'status', 'deadline')
    list_filter = ('status', 'assigned_to')
    search_fields = ('title', 'description')
    inlines = [CompletionReportInline]

admin.site.register(Task, TaskAdmin)
admin.site.register(CompletionReport)