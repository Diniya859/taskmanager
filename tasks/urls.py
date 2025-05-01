from django.urls import path
from .views import TaskCreateView, TaskListView, TaskDetailView, CompletionReportListView

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('reports/', CompletionReportListView.as_view(), name='completion-reports'),
]