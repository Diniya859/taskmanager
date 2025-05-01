from rest_framework import serializers
from tasks.models import Task
from users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_by = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'assigned_to', 'assigned_by',
            'status', 'created_at', 'updated_at', 'due_date',
            'completion_report', 'worked_hours'
        ]
        read_only_fields = [
            'assigned_by', 'created_at', 'updated_at',
            'completion_report', 'worked_hours'
        ]

class TaskUpdateSerializer(serializers.ModelSerializer):
    completion_report = serializers.CharField(required=False)
    worked_hours = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        min_value=0.1
    )

    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']

    def validate(self, data):
        if data.get('status') == TaskStatus.COMPLETED:
            if not data.get('completion_report'):
                raise serializers.ValidationError(
                    "Completion report is required when marking task as completed."
                )
            if not data.get('worked_hours'):
                raise serializers.ValidationError(
                    "Worked hours is required when marking task as completed."
                )
        return data

class TaskReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['completion_report', 'worked_hours']