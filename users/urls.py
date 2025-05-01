from django.urls import path
from .views import TaskListView, TaskDetailView, TaskCompletionReportView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/completion-report/', TaskCompletionReportView.as_view(), name='task-completion-report'),
]