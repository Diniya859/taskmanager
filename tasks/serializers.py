from rest_framework import serializers
from .models import Task, CompletionReport
from users.models import CustomUser


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['assigned_by', 'created_at', 'updated_at']


class CompletionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletionReport
        fields = '__all__'
        read_only_fields = ['submitted_at']


class TaskWithReportSerializer(serializers.ModelSerializer):
    completion_report = CompletionReportSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'