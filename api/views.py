from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from users.models import CustomUser
from tasks.models import Task, TaskStatus
from .serializers import TaskSerializer, TaskUpdateSerializer, TaskReportSerializer


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == CustomUser.Role.SUPERADMIN


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [CustomUser.Role.ADMIN,
                                                                       CustomUser.Role.SUPERADMIN]


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == CustomUser.Role.USER


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]  # This ensures user is logged in

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        return TaskSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Task.objects.none()

        if user.role == CustomUser.Role.SUPERADMIN:
            return Task.objects.all()
        elif user.role == CustomUser.Role.ADMIN:
            return Task.objects.filter(assigned_by=user) | Task.objects.filter(assigned_to__assigned_admin=user)
        return Task.objects.filter(assigned_to=user)

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [IsAdmin]
        elif self.action in ['update', 'partial_update', 'complete']:
            self.permission_classes = [IsUser]
        elif self.action == 'report':
            self.permission_classes = [IsAdmin | IsSuperAdmin]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

    @action(detail=True, methods=['put'])
    def complete(self, request, pk=None):
        task = self.get_object()
        if task.assigned_to != request.user:
            return Response(
                {'error': 'You can only complete your own tasks'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TaskUpdateSerializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data.get('status') != TaskStatus.COMPLETED:
            return Response(
                {'error': 'Status must be set to COMPLETED'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)

        if task.status != TaskStatus.COMPLETED:
            return Response(
                {'error': 'Task is not completed'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not task.completion_report or not task.worked_hours:
            return Response(
                {'error': 'No completion report available for this task'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskReportSerializer(task)
        return Response(serializer.data)