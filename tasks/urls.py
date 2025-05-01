from django.urls import path
from .views import TaskListView, TaskDetailView, TaskCompletionReportView

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('<int:pk>/report/', TaskCompletionReportView.as_view(), name='task-report'),
]