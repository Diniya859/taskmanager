from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from users.models import CustomUser
from .models import Task
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskCompletionReportSerializer
)

from django.shortcuts import render


def task_list(request):
    user = request.user
    if user.role == user.Role.USER:
        tasks = Task.objects.filter(assigned_to=user)
    elif user.role == user.Role.ADMIN:
        tasks = Task.objects.filter(assigned_by=user) | Task.objects.filter(assigned_to__assigned_admin=user)
    else:  # SuperAdmin
        tasks = Task.objects.all()

    context = {
        'tasks': tasks,
        'user': user,
        'is_admin': user.role in [user.Role.ADMIN, user.Role.SUPERADMIN]
    }
    return render(request, 'task.html', context)
class TaskListView(APIView):
    """
    GET /tasks: Fetch all tasks assigned to the logged-in user
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Only return tasks assigned to the requesting user
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskDetailView(APIView):
    """
    PUT /tasks/{id}: Users can update task status
    - When updating to Completed, requires Completion Report and Worked Hours
    """
    permission_classes = [IsAuthenticated]

    def get_task(self, pk, user):
        """Helper method to get task with permission check"""
        try:
            task = Task.objects.get(pk=pk)
            if task.assigned_to != user:
                raise PermissionDenied("You can only access tasks assigned to you")
            return task
        except Task.DoesNotExist:
            raise NotFound("Task not found")

    def get(self, request, pk):
        """GET task details (not in requirements but useful)"""
        task = self.get_task(pk, request.user)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        """Update task status"""
        task = self.get_task(pk, request.user)
        serializer = TaskUpdateSerializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            # Additional validation for completion report
            new_status = serializer.validated_data.get('status', task.status)
            if new_status == 'COMPLETED':
                if not serializer.validated_data.get('completion_report'):
                    raise ValidationError(
                        {"completion_report": "This field is required when marking task as completed"}
                    )
                if not serializer.validated_data.get('worked_hours'):
                    raise ValidationError(
                        {"worked_hours": "This field is required when marking task as completed"}
                    )

            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskCompletionReportView(APIView):
    """
    GET /tasks/{id}/report: Admins/SuperAdmins can view Completion Report and Worked Hours
    - Only available for completed tasks
    """
    permission_classes = [IsAuthenticated]

    def get_task(self, pk):
        """Helper method to get task with existence check"""
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise NotFound("Task not found")

    def get(self, request, pk):
        """Get completion report for a task"""
        task = self.get_task(pk)

        # Permission check - only admins/superadmins can view reports
        if not (request.user.is_admin or request.user.is_superadmin):
            raise PermissionDenied(
                "Only admin users can view completion reports"
            )

        # Check if task is completed
        if task.status != 'COMPLETED':
            raise ValidationError(
                {"detail": "Completion report is only available for completed tasks"}
            )

        serializer = TaskCompletionReportSerializer(task)
        return Response(serializer.data)