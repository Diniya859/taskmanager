from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Task, CompletionReport
from .serializers import TaskSerializer, CompletionReportSerializer, TaskWithReportSerializer
from .permissions import IsTaskOwner, CanManageTasks, CanViewCompletionReports
from users.models import CustomUser


class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [CanManageTasks]

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superadmin or user.is_admin:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsTaskOwner | CanManageTasks]

    def get_serializer_class(self):
        if self.request.user.is_admin or self.request.user.is_superadmin:
            return TaskWithReportSerializer
        return TaskSerializer

    def perform_update(self, serializer):
        task = self.get_object()
        new_status = self.request.data.get('status')

        if new_status == 'COMPLETED' and task.status != 'COMPLETED':
            report_text = self.request.data.get('report_text')
            worked_hours = self.request.data.get('worked_hours')

            if not report_text or not worked_hours:
                return Response(
                    {'error': 'Completion report and worked hours are required when marking task as completed.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save(status=new_status)
            CompletionReport.objects.create(
                task=task,
                report_text=report_text,
                worked_hours=worked_hours
            )
        else:
            serializer.save()


class CompletionReportListView(generics.ListAPIView):
    serializer_class = TaskWithReportSerializer
    permission_classes = [CanViewCompletionReports]

    def get_queryset(self):
        return Task.objects.filter(status='COMPLETED')